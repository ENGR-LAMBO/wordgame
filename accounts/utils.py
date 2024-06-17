# myapp/utils.py

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.crypto import get_random_string

def send_activation_email(user, request):
    token = get_random_string(length=32)
    user.email_verification_token = token
    user.save()
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    current_site = get_current_site(request)
    activation_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
    activation_url = f'http://{current_site.domain}{activation_link}'
    subject = 'Activate your account'
    message = render_to_string('accounts/activation_email.html', {
        'user': user,
        'activation_url': activation_url,
    })
    send_mail(subject, message, 'malvlambo@gmail.com', [user.email])




# import logging
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes
# from django.contrib.sites.shortcuts import get_current_site
# from django.urls import reverse
# from .tokens import account_activation_token

# logger = logging.getLogger(__name__)

# def send_activation_email(user, request):
#     current_site = get_current_site(request)
#     activate_url = f"http://{current_site.domain}{reverse('activate', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': account_activation_token.make_token(user)})}"
#     logger.debug(f"Activation URL: {activate_url}")
#     message = render_to_string('accounts/activation_email.html', {
#         'user': user,
#         'activate_url': activate_url,
#     })
#     send_mail('Activate your account', message, 'malvlambo@gmail.com', [user.email])
