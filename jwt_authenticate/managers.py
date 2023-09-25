from django.db.models import Manager
from django.utils import timezone


class NotExpiredActiveManager(Manager):

    def get_queryset(self):
        return super().get_queryset().filter(expired_at__gt=timezone.now(), is_active=True)
