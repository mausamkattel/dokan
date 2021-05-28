from django.core.mail import send_mail
from django.conf import settings


def email(user, subject, message):
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user, ]
    try:
        send_mail(subject, message, email_from, recipient_list)
    except Exception:
        pass
