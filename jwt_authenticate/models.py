from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from jwt_authenticate.managers import NotExpiredActiveManager


User = get_user_model()


class UserLogin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logins', verbose_name=_('user'))
    refresh_token = models.CharField(max_length=1050, verbose_name=_('refresh token'), db_index=True)
    is_active = models.BooleanField(default=True, verbose_name=_('is active'), db_index=True)
    expired_at = models.DateTimeField(db_index=True)
    device = models.CharField(max_length=64, verbose_name=_('device'))
    ip_address = models.GenericIPAddressField(verbose_name=_('ip address'))

    default_manager = models.Manager()
    objects = NotExpiredActiveManager()

    class Meta:
        verbose_name = _('User Login')
        verbose_name_plural = _('User Logins')

    def __str__(self):
        return f'{self.user} - {self.device} - {self.ip_address}'
