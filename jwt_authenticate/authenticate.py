from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.exceptions import InvalidToken

from jwt_authenticate.services import decrypt_token


class CustomAuthentication(JWTAuthentication):

    def get_validated_token(self, raw_token: bytes) -> Token:
        token = decrypt_token(encrypted_token=raw_token)
        if token is None:
            raise InvalidToken(
                {
                    "detail": _("Given token not valid for any token type"),
                }
            )
        return super().get_validated_token(token.encode())
