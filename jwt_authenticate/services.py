from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from typing import ByteString, Dict

from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings

User = get_user_model()


def encrypt_token(token: str, key: ByteString = settings.JWT_KEY) -> str:
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(token.encode('utf-8'), AES.block_size))
    encrypted_token = base64.b64encode(ciphertext).decode('utf-8')
    return encrypted_token


def token_decrypt(encrypted_token: str, key: ByteString = settings.JWT_KEY) -> str:
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = base64.b64decode(encrypted_token)
    decrypted_token = unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')
    return decrypted_token


def get_token(user: User) -> Dict:
    token = RefreshToken.for_user(user=user)

    token['username'] = user.username
    token['email'] = user.email
    token['uuid_field'] = str(user.uuid_field)
    token['first_name'] = user.first_name
    token['last_name'] = user.last_name

    return {
        "refresh": encrypt_token(token=str(token)),
        "access": encrypt_token(token=str(token.access_token)),
    }


def user_login(password: str, user_auth: str) -> Dict | None:
    user = authenticate(username=user_auth, password=password)
    if not user:
        return None

    return get_token(user=user)
