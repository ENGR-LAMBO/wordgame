# accounts/urls.py

# accounts/urls.py

# accounts/urls.py

from django.urls import path
from . import views
from .views import (
    CustomPasswordResetView, 
    CustomLoginView, 
    SignUpView, 
    ActivateAccount,
    ActivateAccountView, 
    DashboardView, 
    CustomPasswordResetConfirmView, 
    LandingPageView, 
    root_redirect,
    activate
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Root redirection
    path('', root_redirect, name='root_redirect'),

    # Authentication paths
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),


    # Dashboard and landing page paths
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('landing/', LandingPageView.as_view(), name='landing_page'),

    # Custom password reset views
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Default Django auth views for password reset process
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # Game views
    path('dashboard/', views.dashboard, name='dashboard'),
    path('levels/', views.levels, name='levels'),
    path('level1/', views.level1, name='level1'),
    path('level2/', views.level2, name='level2'),
    path('level3/', views.level3, name='level3'),
]









