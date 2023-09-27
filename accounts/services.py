from random import randint

from django.contrib.auth import get_user_model

from utils.cache import set_cache, get_cache
from accounts.tasks import send_otp_code
from accounts.models import UserFollow


User = get_user_model()


def get_opt_code() -> str:
    return str(randint(1, 9999))


def user_register(username: str, email: str, password: str, request) -> None:
    code = get_opt_code()

    session_value = {"code": code, "email": email}
    cache_value = {"email": email, "password": password, "username": username}

    request.session['register_info'] = session_value

    set_cache(key=code, value=cache_value, timeout=300)

    send_otp_code.delay(code, [email])

    return None


def create_user_from_cache(code: str) -> User | None:
    cache_info = get_cache(key=code)
    if not cache_info:
        return None

    return User.objects.create_user(
        username=cache_info['username'],
        email=cache_info['email'],
        password=cache_info['password'],
    )


def get_user_by_username(username: str) -> User | None:
    user = User.objects.filter(username=username)
    if user.exists():
        return user.first()
    return None


def user_follow(follower: User, following: User) -> None:
    if not follower.followings.filter(following__id=following.id):
        return UserFollow.objects.create(follower=follower, following=following)


def user_unfollow(follower: User, following: User) -> None:
    user_follow_row = follower.followings.filter(following__id=following.id)
    if user_follow_row.exists():
        user_follow_row.delete()
