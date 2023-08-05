from functools import lru_cache
from logging import getLogger
from typing import Optional

import jwt
from jwt.exceptions import PyJWTError, InvalidTokenError
from keycloak import KeycloakOpenID

from avatar_utils.sso_helper.constants import (
    ITMO_SSO_SERVER,
    ITMO_REALM,
    USER_TOKEN_AUDIENCE,
    PUBLIC_KEY_WRAPPER,
)
from avatar_utils.sso_helper.flask_auth_header import FlaskAuthHeader

logger = getLogger()


class SSOHelper:

    def __init__(self,
                 client_id: str,
                 client_secret: Optional[str] = None,
                 server_url: str = ITMO_SSO_SERVER,
                 verify_token: bool = True):

        self.verify_token = verify_token
        self.auth_header = FlaskAuthHeader()
        self.keycloak_client: KeycloakOpenID = KeycloakOpenID(server_url=server_url,
                                                              client_id=client_id,
                                                              realm_name=ITMO_REALM,
                                                              client_secret_key=client_secret)
        self._public_key: Optional[str] = None

    @property
    def public_key(self) -> str:
        if not self._public_key:
            self._public_key = self.keycloak_client.public_key()
            logger.info(f'RECEIVED PUBLIC KEY:\n{self._public_key}')
        return PUBLIC_KEY_WRAPPER.format(public_key=self._public_key)

    def extract_payload(self,
                        token: str,
                        verify: Optional[bool] = None,
                        raise_exc: bool = False) -> Optional[dict]:

        if verify is None:
            verify = self.verify_token

        if self.verify_token and not self.public_key:
            if raise_exc:
                raise ValueError('***** PUBLIC KEY IS ABSENT *****')
            logger.error('***** PUBLIC KEY IS ABSENT *****')
            return

        try:
            return jwt.decode(token,
                              key=self.public_key,
                              audience=USER_TOKEN_AUDIENCE,
                              verify=verify)
        except (PyJWTError, InvalidTokenError, ValueError) as err:
            logger.warning(f'{err.__class__.__name__}: {token}')
            if raise_exc:
                raise err
            return

    @staticmethod
    def make_token(sso_user_id: str,
                   key: str = 'secret',
                   **payload_fields) -> str:

        payload_fields.update(dict(sub=sso_user_id,
                                   aud=USER_TOKEN_AUDIENCE))
        token = jwt.encode(payload=payload_fields, key=key)
        return token.decode()

    @lru_cache()
    def get_tokens(self, username: str, password: str) -> dict:
        tokens = self.keycloak_client.token(username=username, password=password)

        return tokens

    @lru_cache()
    def get_access_token(self, username: str, password: str):
        tokens = self.get_tokens(username=username, password=password)

        return tokens['access_token']

    @lru_cache()
    def get_user_sso_id(self, username: str, password: str):
        access_token = self.get_access_token(username=username, password=password)

        payload = jwt.decode(access_token,
                             key=self._public_key,
                             audience='account',
                             verify=True)
        return payload['sub']
