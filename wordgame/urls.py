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

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from accounts.views import (
    CustomLoginView, SignUpView, ActivateAccount, DashboardView,
    CustomPasswordResetView, CustomPasswordResetConfirmView,
    root_redirect, LandingPageView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Include the accounts app URLs
    path('', root_redirect, name='root_redirect'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('landing/', LandingPageView.as_view(), name='landing_page'),

    # Password reset paths with custom views
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # 
    path('auth/', include('dj_rest_auth.urls')),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
]





# from django.contrib import admin
# from django.urls import path, include
# from accounts.views import CustomLoginView, SignUpView, ActivateAccount, DashboardView, CustomPasswordResetView, CustomPasswordResetConfirmView
# from accounts import views as accounts_views
# from django.views.generic import RedirectView
# from accounts.views import CustomLoginView
# from accounts.views import LandingPageView



# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', LandingPageView.as_view(), name='landing_page'),
#     path('login/', CustomLoginView.as_view(), name='login'),
#     path('', RedirectView.as_view(url='login/', permanent=False)),  # Redirect requests to the login page
#     path('login/', CustomLoginView.as_view(), name='login'),
#     path('signup/', SignUpView.as_view(), name='signup'),
#     path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
#     path('dashboard/', DashboardView.as_view(), name='dashboard'),
#     path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
#     path('password_reset_confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     # Include any other URL patterns here
#     # path('login/', accounts_views.login_view, name='login'),  # Assuming you have a custom login view
#     # path('dashboard/', accounts_views.dashboard, name='dashboard'),
#     # path('accounts/', include('accounts.urls')),
#     # path('', include('accounts.urls')),
#     # path('', include('django.contrib.auth.urls')),
#     # path('', include('accounts.urls')),
# ]

