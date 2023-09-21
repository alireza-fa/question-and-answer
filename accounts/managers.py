from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, username: str, email: str, password: str) -> object:
        if not username:
            raise ValueError(_('User must have username'))
        elif not email:
            raise ValueError(_('User must have email'))
        elif not password:
            raise ValueError(_('User must have password'))
        user = self.model(
            username=username, email=BaseUserManager.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(self, username: str, email: str, password: str) -> object:
        user = self.create_user(username=username, email=email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None):
        user = self.create_admin(username=username, email=email, password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user
