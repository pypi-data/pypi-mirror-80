"""Declares :class:`EmailService`."""
from django.core.mail import send_mail
from django.conf import settings


class EmailService:
    """Provides an interface to send transactional emails."""

    def send(self, sender, subject, recipients, text, html):
        """Sends an email to the specified recipients."""
        if sender is None:
            sender = settings.DEFAULT_FROM_EMAIL
        return send_mail(subject, text, sender, recipients,
            html_message=html)
