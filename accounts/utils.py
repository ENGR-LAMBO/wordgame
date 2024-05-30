# myapp/utils.py

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings

def password_reset_email(request, user):
    current_site = get_current_site(request)
    mail_subject = 'Password reset on example.com'
    message = render_to_string('password_reset_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'protocol': 'http' if settings.DEBUG else 'https',
    })
    send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [user.email])
