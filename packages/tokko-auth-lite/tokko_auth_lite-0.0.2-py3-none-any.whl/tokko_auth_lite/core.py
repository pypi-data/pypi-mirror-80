from typing import Callable, List, Dict, Any, Type
from dataclasses import dataclass
from contextlib import suppress
import logging
import json
import os

import jwt

log = logging.getLogger(__name__)


@dataclass(init=True)
class Token:
    headers: dict
    payload: dict

    HEADER_KEY: str = "Authorization"
    PERMISSION_KEY: str = "permissions"
    PERMISSION_SEP: str = ","
    TOKEN_PREFIX: str = "Bearer"
    USER_ID: str = "email"
    VALIDATIONS: List[Callable] = None
    ALGORITHMS: str = os.environ.get("TOKKO_AUTH_ALGORITHMS", "RS256")
    AUDIENCE: str = os.environ.get("TOKKO_AUTH_API_AUDIENCE")
    SECRET: str = None

    @classmethod
    def from_jwt(cls, token, algorithms: str = ALGORITHMS, extended=False):
        try:
            unverified_header = jwt.get_unverified_header(token)
            payload = jwt.decode(token, algorithms=algorithms, verify=False)
            if extended:
                return token, Token(payload=payload, headers=unverified_header)
            return Token(payload=payload, headers=unverified_header)
        except jwt.ExpiredSignatureError:
            raise ValueError("Token signature is expired")
        except Exception as token_error:
            raise ValueError(f"Unable decode token. {token_error}")

    @classmethod
    def from_header(cls, headers: Dict[str, Any], key_name=HEADER_KEY, token_prefix=TOKEN_PREFIX, **extras):
        if not isinstance(headers, dict):
            raise TypeError(f"Headers Error. Expected Dict, Got {type(headers)} instead")
        token_header = headers.get(key_name)
        if not token_header:
            raise KeyError(f"Headers Error. Key {key_name} not found")
        token_header = token_header.split()
        if len(token_header) > 2:
            raise ValueError("Token too long")
        if len(token_header) < 2:
            raise ValueError("Token too short")
        if token_prefix.lower() not in token_header[0].lower():
            raise KeyError(f"Token header should start with '{token_prefix}'")
        _, token = token_header
        return cls.from_jwt(token=token,
                            extended=extras.get("extended", False))

    @property
    def user_id(self):
        try:
            return self.payload[self.USER_ID]
        except KeyError:
            raise KeyError("Token USER_ID not found")

    @property
    def permissions(self):
        try:
            permissions = self.payload[self.PERMISSION_KEY]
            if isinstance(permissions, str):
                permissions = permissions.split(self.PERMISSION_SEP)
            with suppress(ValueError):
                del permissions[permissions.index("")]
            log.debug(permissions)
            return permissions
        except KeyError:
            return []

    def has_permission(self, *permission, require_all=False):
        if not require_all:
            return any([perm in self.permissions for perm in permission])
        else:
            return all([perm in self.permissions for perm in permission])

    def as_dict(self):
        return {
            "payload": self.payload,
            "headers": self.headers,
        }

    def __str__(self):
        return json.dumps(self.as_dict())

