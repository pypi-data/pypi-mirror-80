from contextlib import suppress
from unittest import TestCase
import json
import os

from Crypto.PublicKey import RSA

from tokko_auth_lite.tools.testing import (
    TokenHeaders,
    Payload,
    RSAIDManager,
    TokenFabrik,
)
from tokko_auth_lite.core import Token


# def generate_public_key(private_key: str) -> str:
#     key = RSA.import_key(private_key)
#     public_key = key.publickey().export_key()
#     return f"{public_key}"


def create_pem(**options):
    key = RSA.generate(options.get("bytes_length", 2048))
    private_key = key.export_key()
    root_folder = options.get("root_folder", os.path.dirname(os.path.abspath(__file__)))
    filename = os.path.join(root_folder, options.get("filename", "private_key.pem"))
    with open(filename, "wb") as pem_file:
        pem_file.write(private_key)
    return filename, private_key.decode("utf8")


class TokenHeadersTest(TestCase):
    def test_01_token_headers_class(self):
        th = TokenHeaders()
        self.assertEqual(th.kid, "no-kid-provided")
        self.assertEqual(th.extra_headers, None)
        self.assertEqual(f"{th}", json.dumps({"kid": "no-kid-provided"}, indent=4))

    def test_02_token_headers_class(self):
        th = TokenHeaders("my-k-id", extra_headers={"hallo": "welt"})
        self.assertEqual(th.kid, "my-k-id")
        self.assertEqual(type(th.extra_headers), dict)
        self.assertEqual(th.extra_headers, {"hallo": "welt"})

    def test_03_token_headers_class_invalid_extra_headers(self):
        with self.assertRaises(TypeError):
            TokenHeaders(extra_headers="invalid")


class PayloadTests(TestCase):
    def setUp(self) -> None:
        self.payload = Payload()

    def test_04_payload_class(self):
        self.assertEqual(self.payload.scope, "email profile openid")
        self.assertEqual(self.payload.permissions, None)
        self.assertEqual(self.payload.scope, "email profile openid")
        self.assertEqual(self.payload.iss, "https://testing.com/service")
        self.assertEqual(self.payload.aud, "https://testing.provider.com/")
        self.assertEqual(self.payload.gty, "client-credentials")

    def test_05_payload_class_timestamps(self):
        self.assertEqual(self.payload.iat < self.payload.exp, True)

    def test_06_payload_class_output_types(self):
        self.assertEqual(self.payload.as_dict().__class__, dict)
        self.assertEqual(json.loads(f"{self.payload}"), self.payload.as_dict())


class RSAIDManagerTests(TestCase):
    def setUp(self) -> None:
        pem_filename, content = create_pem(filename="test_private_key.pem")
        self.test_pem_file_content = content
        self.test_pem_file = pem_filename

    def tearDown(self) -> None:
        with suppress(IOError):
            os.remove(self.test_pem_file)

    def test_07_rsa_id_manager_class(self):
        rsa_id_manager = RSAIDManager()
        self.assertEqual(rsa_id_manager.private_key is not None, True)
        self.assertEqual(rsa_id_manager.public_key is not None, True)
        self.assertEqual(type(rsa_id_manager.private_key), str)
        self.assertEqual(type(rsa_id_manager.public_key), bytes)

    def test_08_rsa_id_manager_class_jwks(self):
        rsa_id_manager = RSAIDManager()
        self.assertEqual(len(rsa_id_manager.jwks), 1)
        self.assertEqual(type(rsa_id_manager.jwks), dict)

    def test_09_rsa_id_manager_from_file(self):
        rsa_manager = RSAIDManager.load_pem_from_file(pem_filename=self.test_pem_file)
        self.assertEqual(rsa_manager.private_key, self.test_pem_file_content)
        self.assertEqual(rsa_manager.public_key is not None, True)
        self.assertEqual(type(rsa_manager.public_key), bytes)

    def test_10_rsa_id_manager_invalid_content(self):
        with self.assertRaises(TypeError):
            RSAIDManager(private_key_pem=1)


class TokenFabrikTests(TestCase):
    def setUp(self) -> None:
        pem_filename, content = create_pem(filename="test_private_key.pem")
        self.test_pem_file_content = content
        self.test_pem_file = pem_filename

    def tearDown(self) -> None:
        with suppress(IOError):
            os.remove(self.test_pem_file)

    def test_11_fabrik_instance(self):
        tf = TokenFabrik(private_key_pem=self.test_pem_file_content)
        self.assertEqual(tf.algorithm, "RS256")
        self.assertEqual(tf.pk_bits, 1024)
        self.assertEqual(tf.private_key, self.test_pem_file_content)

    def test_12_token_fabrik_public_key(self):
        tf = TokenFabrik(private_key_pem=self.test_pem_file_content)
        self.assertEqual(type(tf.public_key), bytes)
        self.assertEqual(len(tf.public_key) > 10, True)
        self.assertEqual(
            {tf.auth_header_key_name: f"Bearer {tf.token}",}, tf.authorization_header()
        )


class TokenTests(TestCase):
    def setUp(self) -> None:
        self.token_fabrik = TokenFabrik()
        pem_filename, content = create_pem(filename="test_private_key.pem")
        self.test_pem_file_content = content
        self.test_pem_file = pem_filename

    def tearDown(self) -> None:
        with suppress(IOError):
            os.remove(self.test_pem_file)

    def test_13_token_instance(self):
        token = Token(
            payload=self.token_fabrik.payload, headers=self.token_fabrik.headers,
        )
        self.assertEqual(token.permissions, [])
        self.assertEqual(type(token.payload), dict)
        self.assertEqual(len(token.payload), 7)
        self.assertEqual(token.payload, self.token_fabrik.payload)
        self.assertEqual(token.is_valid(), True)
        with self.assertRaises(KeyError):
            uid = token.user_id

    def test_14_token_class(self):
        self.assertEqual(Token.TOKEN_PREFIX, "Bearer")
        self.assertEqual(Token.HEADER_KEY, "Authorization")
        self.assertEqual(Token.PERMISSION_SEP, ",")
        self.assertEqual(Token.PERMISSION_KEY, "permissions")
        self.assertEqual(
            Token.from_header(self.token_fabrik.authorization_header()),
            Token.from_jwt(self.token_fabrik.token),
        )
        with self.assertRaises(ValueError):
            Token.from_jwt(1)

    def test_15_token_permission(self):
        permission = ["spacex:launch_rockets", "spacex:reach_the_moon"]
        fabrik = TokenFabrik(permission=permission)
        token = Token(payload=fabrik.payload, headers=fabrik.headers,)
        self.assertEqual(token.permissions, permission)
        token.PERMISSION_KEY = "invalid"
        self.assertEqual(token.permissions, [])

    def test_16_token_has_permission(self):
        permission = ["spacex:launch_rockets", "spacex:reach_the_moon"]
        fabrik = TokenFabrik(permission=permission)
        token = Token(payload=fabrik.payload, headers=fabrik.headers,)
        self.assertEqual(token.has_permission("spacex:reach_the_moon"), True)
        self.assertEqual(
            token.has_permission("spacex:reach_the_moon", "spacex:conquer_the_world"),
            True,
        )
        self.assertEqual(
            token.has_permission(
                "spacex:reach_the_moon", "spacex:be_an_asshole", require_all=True
            ),
            False,
        )

    def test_17_token_representations(self):
        token = Token(payload=self.token_fabrik.payload, headers=self.token_fabrik.headers)
        self.assertEqual(
            token.as_dict(),
            {
                "payload": self.token_fabrik.payload,
                "headers": self.token_fabrik.headers
            }
        )
        self.assertEqual(f"{token}", json.dumps(token.as_dict()))
        with self.assertRaises(KeyError):
            Token.from_header({"Authorization": "Bad Token"})
        with self.assertRaises(ValueError):
            Token.from_header({"Authorization": "ShortToken"})
        with self.assertRaises(ValueError):
            Token.from_header({"Authorization": "Too long Token"})
        with self.assertRaises(KeyError):
            Token.from_header({})
        with self.assertRaises(TypeError):
            Token.from_header("invalid-headers")
