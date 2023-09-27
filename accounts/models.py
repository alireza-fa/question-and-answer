from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=64,
        unique=True,
        help_text=_(
            'Required. 64 characters or fewer. Letters, digits and @/./+/-/_ only.'
        ),
        verbose_name=_('username'),
        db_index=True,
        validators=[username_validator],
        error_messages={
            "unique": _('A user with that username already exists.'),
        },
    )
    email = models.EmailField(max_length=120, unique=True, verbose_name=_('email'), db_index=True)
    first_name = models.CharField(max_length=34, null=True, blank=True, verbose_name=_('first name'))
    last_name = models.CharField(max_length=34, null=True, blank=True, verbose_name=_('last name'))
    is_active = models.BooleanField(default=True, verbose_name=_('is active'))
    is_admin = models.BooleanField(default=False, verbose_name=_('is admin'))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return f'{self.username} - {self.email}'

    def is_staff(self):
        return self.is_admin

    def get_fullname(self):
        return f'{self.first_name} {self.last_name}'


class UserFollow(models.Model):
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followings', verbose_name=_('follower'))
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers', verbose_name=_('following'))
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('User Follow')
        verbose_name_plural = _('User Follows')

    def __str__(self):
        return f'{self.follower} --> {self.following}'
