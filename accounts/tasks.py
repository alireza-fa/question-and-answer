from typing import List

from django.utils.translation import gettext_lazy as _
from celery import shared_task

from utils.email_service.send import send_email


@shared_task
def send_otp_code(code: str, emails: List) -> int:
    subject = _('Otp Code')
    body = code
    return send_email(subject=subject, body=body, receivers=emails)
