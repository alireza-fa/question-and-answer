import binascii

from Crypto.Cipher import AES
from Crypto.Cipher._mode_ecb import EcbMode
from Crypto.Util.Padding import pad, unpad
import base64
from typing import ByteString, Dict

from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, Token, UntypedToken
from django.conf import settings
from django.utils import timezone

from jwt_authenticate.models import UserLogin


User = get_user_model()


def set_refresh_expired_at():
    return timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']


def get_new_cipher(key: ByteString) -> EcbMode:
    return AES.new(key, AES.MODE_ECB)


def ciphertext_encrypt(cipher: EcbMode, token: str) -> ByteString:
    return cipher.encrypt(pad(token.encode('utf-8'), AES.block_size))


def ciphertext_decode(encrypted_token: ByteString) -> bytes | None:
    try:
        cipher_decode = base64.b64decode(encrypted_token)
    except binascii.Error:
        return None
    else:
        return cipher_decode


def encrypt_token(token: str, key: ByteString = settings.JWT_KEY) -> str:
    cipher = get_new_cipher(key=key)
    ciphertext = ciphertext_encrypt(cipher=cipher, token=token)
    encrypted_token = base64.b64encode(ciphertext).decode('utf-8')
    return encrypted_token


def decrypt_token(encrypted_token: ByteString, key: ByteString = settings.JWT_KEY) -> str | None:
    cipher = get_new_cipher(key=key)
    ciphertext = ciphertext_decode(encrypted_token=encrypted_token)
    if ciphertext is None:
        return None
    decrypted_token = unpad(cipher.decrypt(ciphertext), AES.block_size).decode('utf-8')
    return decrypted_token


def get_client_ip(request: object) -> str:
    x_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forward_for:
        ip = x_forward_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_client_info(request: object) -> Dict:
    return {
        "device_name": request.META.get('HTTP_USER_AGENT', ''),
        "ip_address": get_client_ip(request=request)
    }


def set_token_claims(token: Token, user: User, client_info: Dict) -> Token:
    token['username'] = user.username
    token['email'] = user.email
    token['first_name'] = user.first_name
    token['last_name'] = user.last_name
    token['device_name'] = client_info['device_name']
    token['ip_address'] = client_info['ip_address']

    return token


def get_token(user: User, request: object, client_info: Dict) -> Dict:
    token = RefreshToken.for_user(user=user)

    token = set_token_claims(token=token, user=user, client_info=client_info)

    return {
        "refresh": encrypt_token(token=str(token)),
        "access": encrypt_token(token=str(token.access_token)),
    }


def create_user_login(user: User, token: Dict, client_info: Dict) -> UserLogin:
    return UserLogin.objects.create(
        user=user,
        refresh_token=token['refresh'],
        device=client_info['device_name'],
        expired_at=set_refresh_expired_at(),
        ip_address=client_info['ip_address'],
    )


def user_login(password: str, user_auth: str, request: object) -> Dict | None:
    user = authenticate(username=user_auth, password=password)
    if not user:
        return None

    client_info = get_client_info(request=request)

    token = get_token(user=user, request=request, client_info=client_info)

    create_user_login(user=user, token=token, client_info=client_info)

    return token


def get_user_login(refresh_token: ByteString) -> UserLogin | None:
    user_log = UserLogin.objects.filter(refresh_token=refresh_token)
    if not user_log.exists():
        return None
    return user_log.first()


def set_access_token(refresh_token: str) -> str | None:
    try:
        token = RefreshToken(token=refresh_token)
    except TokenError:
        return None

    access = str(token.access_token)

    return encrypt_token(token=access)


def verify_user_token(user_log: UserLogin, r_client_info: Dict) -> bool:
    if user_log.device != r_client_info['device_name'] or user_log.ip_address != r_client_info['ip_address']:
        return False
    return True


def verify_token(token: Token, r_client_info: Dict) -> bool:
    if token['device_name'] != r_client_info['device_name'] or token['ip_address'] != r_client_info['ip_address']:
        return False
    return True


def get_access_token(refresh_token: ByteString, request) -> str | None:
    r_client_info = get_client_info(request)

    refresh_token_decrypt = decrypt_token(encrypted_token=refresh_token)
    if refresh_token_decrypt is None:
        return None

    user_log = get_user_login(refresh_token=refresh_token)
    if user_log is None:
        return None

    if verify_user_token(user_log=user_log, r_client_info=r_client_info) is False:
        return None

    return set_access_token(refresh_token=refresh_token_decrypt)


def check_validate_token(encrypted_token: ByteString, request) -> bool:
    decrypted_token = decrypt_token(encrypted_token=encrypted_token)
    if decrypted_token is None:
        return False

    try:
        token = UntypedToken(token=decrypted_token)
    except TokenError:
        return False

    r_client_info = get_client_info(request=request)

    if token['exp'] <= timezone.now().timestamp():
        return False

    if verify_token(token=token, r_client_info=r_client_info) is False:
        return False

    if token['token_type'] == 'refresh':
        user_log = get_user_login(refresh_token=encrypted_token)
        if user_log is None:
            return False

    return True
