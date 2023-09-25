from typing import List

from django.core.mail import send_mail
from django.conf import settings

from utils.cache import set_cache, get_cache, incr


def send_email(
        subject: str,
        body: str,
        receivers: List,
        sender: str = settings.DEFAULT_FROM_EMAIL,
) -> int:
    for receiver in receivers:
        key = receiver + '_count'
        email_count = get_cache(key=key)

        if not email_count:
            set_cache(key=key, value=1, timeout=86400)
            email_count = get_cache(key=key)

        if int(email_count) >= 5:
            return 200

        incr(key=key)

        return send_mail(
            subject=subject,
            message=body,
            from_email=sender,
            recipient_list=[receiver],
            fail_silently=True
        )
