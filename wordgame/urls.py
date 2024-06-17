"""
URL configuration for wordgame project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# wordgame/urls.py

# wordgame/urls.py

from django.contrib import admin
from django.urls import path
from accounts.views import (
    CustomLoginView, 
    SignUpView, 
    CustomPasswordResetView, 
    CustomPasswordResetConfirmView, 
    DashboardView, 
    ActivateAccount, 
    LandingPageView,
    root_redirect,
    levels,
    level1,
    level2,
    level3
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('', root_redirect, name='root_redirect'),
    path('', LandingPageView.as_view(), name='landing_page'),  # Ensure this line is present
    path('levels/', levels, name='levels'),
    path('levels/1/', level1, name='level1'),
    path('levels/2/', level2, name='level2'),
    path('levels/3/', level3, name='level3'),
]





# from django.contrib import admin
# from django.urls import path, include
# from django.contrib.auth import views as auth_views
# from accounts.views import (
#     CustomLoginView, SignUpView, ActivateAccount, ActivateAccountView, DashboardView,
#     CustomPasswordResetView, CustomPasswordResetConfirmView,
#     root_redirect, LandingPageView
# )

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('accounts/', include('accounts.urls')),  # Include the accounts app URLs

#     # Root redirection
#     path('', root_redirect, name='root_redirect'),

#     # Authentication paths
#     path('login/', CustomLoginView.as_view(), name='login'),
#     path('signup/', SignUpView.as_view(), name='signup'),
#     path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),

#     # Password reset paths with custom views
#     path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
#     path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
#     path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

#     # Dashboard and landing page
#     path('dashboard/', DashboardView.as_view(), name='dashboard'),
#     path('landing/', LandingPageView.as_view(), name='landing_page'),

#     # Authentication and registration paths using dj_rest_auth
#     path('auth/', include('dj_rest_auth.urls')),
#     path('auth/registration/', include('dj_rest_auth.registration.urls')),
# ]






