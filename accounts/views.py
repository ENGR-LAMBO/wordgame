# accounts/views.py
# accounts/views.py

# # accounts/views.py

from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.generic import TemplateView, View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import get_user_model
from .forms import CustomUserCreationForm  
import hashlib
import os

from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm

User = get_user_model()

def send_activation_email(user, request):
    current_site = get_current_site(request)
    mail_subject = 'Activate your account.'
    activate_url = f"http://{current_site.domain}{reverse('activate', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': default_token_generator.make_token(user)})}"
    message = render_to_string('accounts/activation_email.html', {
        'user': user,
        'activate_url': activate_url,
    })
    send_mail(mail_subject, message, 'malvlambo@gmail.com', [user.email])

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = CustomAuthenticationForm

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user is not None:
            if self.is_user_verified(user.email):
                login(self.request, user)
                return redirect(self.get_success_url())
            else:
                messages.error(self.request, 'Please verify your email before logging in.')
                return self.form_invalid(form)
        else:
            messages.error(self.request, 'Invalid username or password.')
            return self.form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('dashboard')

    def is_user_verified(self, email):
        try:
            with open(settings.VERIFIED_USERS_FILE, 'r') as file:
                for line in file:
                    if email in line:
                        return True
            return False
        except FileNotFoundError:
            return False

class LandingPageView(TemplateView):
    template_name = 'accounts/landing.html'

def generate_activation_token(email):
    # Generate a unique token using the email and a random salt
    salt = os.urandom(16)
    return hashlib.sha256(salt + email.encode()).hexdigest()

def send_activation_email(user, request):
    token = generate_activation_token(user.email)
    activation_link = f"https://wordgame-3snk.onrender.com/activate/{token}/"
    # Implement your email sending logic here
    # Example: send_mail('Account Activation', f'Activate your account: {activation_link}', 'from@example.com', [user.email])
    print(f'Send email to {user.email} with activation link: {activation_link}')

    # Save the token to the user
    user.activation_token = token
    user.save()

class SignUpView(View):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()
            
            # Send an email to the user with the token
            send_activation_email(user, request)
            return render(request, 'accounts/activation_sent.html')

        return render(request, self.template_name, {'form': form})
class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if self.is_user_verified(email):
            users = self.get_users(email)
            if users:
                for user in users:
                    self.send_password_reset_email(user)
            return super().form_valid(form)
        else:
            messages.error(self.request, 'This email is not registered or verified.')
            return self.form_invalid(form)

    def get_users(self, email):
        active_users = User._default_manager.filter(email__iexact=email, is_active=True)
        return (u for u in active_users if u.has_usable_password())

    def send_password_reset_email(self, user):
        current_site = get_current_site(self.request)
        mail_subject = 'Password reset'
        message = render_to_string('accounts/password_reset_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
            'protocol': 'http' if settings.DEBUG else 'https',
        })
        send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [user.email])

    def is_user_verified(self, email):
        try:
            with open(settings.VERIFIED_USERS_FILE, 'r') as file:
                for line in file:
                    if email in line:
                        return True
            return False
        except FileNotFoundError:
            return False

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset_confirm.html'
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('password_reset_complete')

class ActivateAccount(View):
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            # Save user data to a file after activation
            with open(settings.VERIFIED_USERS_FILE, 'a') as f:
                f.write(f'{user.email}, {user.first_name}, {user.last_name}\n')

            messages.success(request, 'Your account has been activated successfully. You can now log in.')
            return redirect('login')
        else:
            return render(request, 'accounts/activation_failure.html')
    
@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'accounts/dashboard.html'

def dashboard_view(request):
    return render(request, 'dashboard.html')

def root_redirect(request):
    return redirect('login')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')

def levels(request):
    return render(request, 'accounts/levels.html')

def level1(request):
    return render(request, 'accounts/level1.html')

def level2(request):
    return render(request, 'accounts/level2.html')

def level3(request):
    return render(request, 'accounts/level3.html')

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        return render(request, 'accounts/activation_invalid.html')




# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User
# from django.utils.http import urlsafe_base64_decode
# from django.utils.encoding import force_str
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.auth import login
# from django.http import HttpResponse
# from django.contrib.auth import authenticate, login, get_user_model
# from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView
# from django.contrib.auth.forms import PasswordResetForm
# from django.contrib.sites.shortcuts import get_current_site
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.urls import reverse_lazy
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_str
# from django.views.generic import TemplateView, View
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
# from django.contrib import messages
# from django.urls import reverse
# from django.conf import settings

# from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordResetForm, CustomSetPasswordForm

# User = get_user_model()

# # def send_activation_email(user, request):
# #     current_site = get_current_site(request)
# #     token = default_token_generator.make_token(user)
# #     uid = urlsafe_base64_encode(force_bytes(user.pk))
# #     activation_link = request.build_absolute_uri(
# #         reverse('activate', kwargs={'uidb64': uid, 'token': token})
# #     )
# #     subject = 'Activate your WordGame account'
# #     message = render_to_string('account_activation_email.html', {
# #         'user': user,
# #         'domain': current_site.domain,
# #         'uid': uid,
# #         'token': token,
# #         'activation_link': activation_link,
# # })
# def send_activation_email(user, request):
#     current_site = get_current_site(request)
#     mail_subject = 'Activate your account.'
#     activate_url = f"http://{current_site.domain}{reverse('activate', kwargs={'uidb64': urlsafe_base64_encode(force_bytes(user.pk)), 'token': account_activation_token.make_token(user)})}"
#     message = render_to_string('accounts/activation_email.html', {
#         'user': user,
#         'activate_url': activate_url,
#     })
#     send_mail(mail_subject, message, 'malvlambo@gmail.com', [user.email])

# class CustomLoginView(LoginView):
#     template_name = 'accounts/login.html'
#     form_class = CustomAuthenticationForm

#     def form_valid(self, form):
#         user = authenticate(
#             username=form.cleaned_data['username'],
#             password=form.cleaned_data['password']
#         )
#         if user is not None:
#             if self.is_user_verified(user.email):
#                 login(self.request, user)
#                 return redirect(self.get_success_url())
#             else:
#                 messages.error(self.request, 'Please verify your email before logging in.')
#                 return self.form_invalid(form)
#         else:
#             messages.error(self.request, 'Invalid username or password.')
#             return self.form_invalid(form)

#     def get_success_url(self):
#         return reverse_lazy('dashboard')

#     def is_user_verified(self, email):
#         try:
#             with open(settings.VERIFIED_USERS_FILE, 'r') as file:
#                 for line in file:
#                     if email in line:
#                         return True
#             return False
#         except FileNotFoundError:
#             return False

# class LandingPageView(TemplateView):
#     template_name = 'accounts/landing.html'

# class SignUpView(View):
#     form_class = CustomUserCreationForm
#     template_name = 'accounts/signup.html'
#     success_url = reverse_lazy('login')

#     def get(self, request, *args, **kwargs):
#         form = self.form_class()
#         return render(request, self.template_name, {'form': form})

#     def post(self, request, *args, **kwargs):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False  # Deactivate account till it is confirmed
#             user.save()
            
#             # Send an email to the user with the token:
#             mail_subject = 'Activate your account.'
#             message = render_to_string('accounts/activation_email.html', {
#                 'user': user,
#                 'domain': request.META['HTTP_HOST'],
#                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#                 'token': default_token_generator.make_token(user),
#             })
#             send_mail(mail_subject, message, 'malvlambo@gmail.com', [user.email])
#             return render(request, 'accounts/activation_sent.html')

#         return render(request, self.template_name, {'form': form})

# class CustomPasswordResetView(PasswordResetView):
#     template_name = 'accounts/password_reset.html'
#     email_template_name = 'accounts/password_reset_email.html'
#     form_class = PasswordResetForm
#     success_url = reverse_lazy('password_reset_done')

#     def form_valid(self, form):
#         email = form.cleaned_data['email']
#         if self.is_user_verified(email):
#             users = self.get_users(email)
#             if users:
#                 for user in users:
#                     self.send_password_reset_email(user)
#             return super().form_valid(form)
#         else:
#             messages.error(self.request, 'This email is not registered or verified.')
#             return self.form_invalid(form)

#     def get_users(self, email):
#         active_users = User._default_manager.filter(email__iexact=email, is_active=True)
#         return (u for u in active_users if u.has_usable_password())

#     def send_password_reset_email(self, user):
#         current_site = get_current_site(self.request)
#         mail_subject = 'Password reset'
#         message = render_to_string('accounts/password_reset_email.html', {
#             'user': user,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': default_token_generator.make_token(user),
#             'protocol': 'http' if settings.DEBUG else 'https',
#         })
#         send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [user.email])

#     def is_user_verified(self, email):
#         try:
#             with open(settings.VERIFIED_USERS_FILE, 'r') as file:
#                 for line in file:
#                     if email in line:
#                         return True
#             return False
#         except FileNotFoundError:
#             return False

# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'accounts/password_reset_confirm.html'
#     form_class = CustomSetPasswordForm
#     success_url = reverse_lazy('password_reset_complete')

# class ActivateAccount(View):
#     def get(self, request, uidb64, token, *args, **kwargs):
#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None

#         if user is not None and default_token_generator.check_token(user, token):
#             user.is_active = True
#             user.save()

#             # Save user data to a file after activation
#             with open(settings.VERIFIED_USERS_FILE, 'a') as f:
#                 f.write(f'{user.email}, {user.first_name}, {user.last_name}\n')

#             messages.success(request, 'Your account has been activated successfully. You can now log in.')
#             return redirect('login')
#         else:
#             return render(request, 'accounts/activation_failure.html')
    
# @method_decorator(login_required, name='dispatch')
# class DashboardView(TemplateView):
#     template_name = 'accounts/dashboard.html'

# def dashboard_view(request):
#     return render(request, 'dashboard.html')

# def root_redirect(request):
#     return redirect('login')

# def dashboard(request):
#     return render(request, 'accounts/dashboard.html')

# def levels(request):
#     return render(request, 'accounts/levels.html')

# def level1(request):
#     return render(request, 'accounts/level1.html')

# def level2(request):
#     return render(request, 'accounts/level2.html')

# def level3(request):
#     return render(request, 'accounts/level3.html')

# def activate(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user is not None and default_token_generator.check_token(user, token):
#         user.is_active = True
#         user.save()
#         return redirect('login')
#     else:
#         return render(request, 'accounts/activation_invalid.html')









