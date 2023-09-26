from django.contrib.auth import get_user_model


class UserEmailAuthBackend:

    def authenticate(self, request, username, password):
        try:
            user = get_user_model().objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(id=user_id)
        except get_user_model().DoesNotExist:
            return None
