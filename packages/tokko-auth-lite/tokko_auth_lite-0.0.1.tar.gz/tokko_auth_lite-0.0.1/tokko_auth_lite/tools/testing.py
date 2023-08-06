from dataclasses import dataclass
import json
import os

from Crypto.PublicKey import RSA
from arrow import get as _, now
from typing import Union, List
from jose import jwt
import jwcrypto.jwk as jwk

ListOrDict = Union[dict, list]


@dataclass
class TokenHeaders:
    kid: Union[int, str] = "no-kid-provided"
    extra_headers: dict = None

    def as_dict(self) -> dict:
        headers = self.extra_headers or {}
        headers.update({"kid": self.kid})
        return headers

    def __post_init__(self):
        if self.extra_headers and not isinstance(self.extra_headers, dict):
            raise TypeError("Unsupported extra-headers instance")

    def __str__(self) -> str:
        return json.dumps(self.as_dict(), indent=4)


@dataclass
class Payload:
    """Payload interface"""

    # Testing constants
    DEFAULT_SCOPE = "email profile openid"
    PERMISSION = []
    DEFAULT_AUD = "https://testing.provider.com/"
    DEFAULT_GTY = "client-credentials"
    DEFAULT_ISS = "https://testing.com/service"

    __epoch__ = _("1970-01-01")
    __now__ = now()

    scope: str = DEFAULT_SCOPE
    permissions: List[str] = None
    expiration_minutes: int = 24 * 60  # Token expires in 1 day.
    aud: str = DEFAULT_AUD
    iss: str = DEFAULT_ISS
    gty: str = DEFAULT_GTY

    extra_claim: dict = None

    @property
    def iat(self) -> int:
        return round((self.__now__ - self.__epoch__).total_seconds())

    @property
    def exp(self) -> int:
        _n = self.__now__
        return round((_n.shift(minutes=self.expiration_minutes) - self.__epoch__).total_seconds())

    def as_dict(self) -> dict:
        permissions = ",".join(self.permissions or [])
        claims = {
            "scope": self.scope,
            "permissions": permissions,
            "iss": self.iss,
            "aud": self.aud or "",
            "iat": self.iat,
            "exp": self.exp,
            "gty": self.gty,
        }
        claims.update(self.extra_claim or {})
        return claims

    def __str__(self) -> str:
        return json.dumps(self.as_dict(), indent=4)


FilePath = str
PrivateKey = str
RSAKey = Union[FilePath, PrivateKey]


@dataclass(init=True)
class RSAIDManager:

    private_key_pem: RSAKey = None
    pk_bits: int = 1024

    __public_key__ = None
    __private_key__ = None

    @property
    def public_key(self):
        return self.__public_key__

    @property
    def private_key(self):
        return self.__private_key__

    @property
    def jwks(self):
        _keys = json.loads(jwk.JWK.from_pem(self.public_key).export())
        _keys.update({"use": "access"})
        return {
            "keys": [_keys]
        }

    @classmethod
    def load_pem_from_file(cls, pem_filename: str, root_folder: FilePath = None):
        pem_file = os.path.join(root_folder or "", pem_filename)
        with open(pem_file, "rb") as pkf:
            private_key = pkf.read()
        return RSAIDManager(private_key_pem=private_key.decode("utf8"))

    def load_rsa(self):
        if not self.private_key_pem:
            rsa_key = RSA.generate(bits=self.pk_bits)
        else:
            if not isinstance(self.private_key_pem, str):
                raise TypeError(f"PrivateKeyPem expected str got {type(self.private_key_pem)} instead")
            rsa_key = RSA.importKey(self.private_key_pem)
        self.__private_key__ = rsa_key.export_key().decode()
        self.__public_key__ = rsa_key.publickey().exportKey('PEM')
        return self.private_key

    def __post_init__(self):
        self.load_rsa()


@dataclass
class TokenFabrik:

    pk_bits: int = 1024
    private_key_pem: str = None
    load_pem_from_file: bool = False

    headers: dict = None
    payload: dict = None
    algorithm: str = "RS256"
    permission: list = None
    extra_claims: dict = None
    auth_header_key_name = "Authorization"
    __token__ = None
    __rsa_id__: RSAIDManager = None
    __initialized__ = False

    @staticmethod
    def build_token(payload: ListOrDict, rsa_id: str, algorithm: str, headers: dict):
        return jwt.encode(
            payload,
            key=rsa_id,
            algorithm=algorithm,
            headers=headers,
        )

    def __initialize_headers__(self):
        headers = self.headers or {}
        headers.update({"use": "access"})
        self.headers = TokenHeaders(kid=self.jwks["keys"][0]["kid"],
                                    extra_headers=headers).as_dict()

    def __initialize_payload__(self):
        payload = self.payload or {}
        self.payload = Payload(permissions=self.permission,
                               extra_claim=self.extra_claims,
                               aud=os.environ.get("API_AUDIENCE"),
                               **payload).as_dict()

    def __initialize_rsa_id__(self):
        self.__rsa_id__ = RSAIDManager(private_key_pem=self.private_key_pem,
                                       pk_bits=self.pk_bits)

    def initialize(self):
        if not self.__initialized__:
            self.__initialize_rsa_id__()
            self.__initialize_headers__()
            self.__initialize_payload__()
            self.__initialized__ = True

    def __post_init__(self):
        self.initialize()

    def authorization_header(self) -> dict:
        return {self.auth_header_key_name: self.bearer}

    @property
    def private_key(self):
        return self.__rsa_id__.private_key

    @property
    def public_key(self):
        return self.__rsa_id__.public_key

    @property
    def jwks(self):
        return self.__rsa_id__.jwks

    @property
    def bearer(self):
        return f"Bearer {self.token}"

    @property
    def token(self):
        if not self.__token__:
            self.__token__ = self.build_token(payload=self.payload,
                                              headers=self.headers,
                                              rsa_id=self.private_key,
                                              algorithm=self.algorithm)
        return self.__token__

