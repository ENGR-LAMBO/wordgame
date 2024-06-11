# accounts/signals.py

from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from allauth.account.utils import send_email_confirmation

@receiver(user_signed_up)
def user_signed_up_(request, user, **kwargs):
    user.is_active = False
    user.save()
    send_email_confirmation(request, user)
