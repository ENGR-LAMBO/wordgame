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
)
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Root redirection
    path('', root_redirect, name='root_redirect'),
    
    # Landing page
    path('landing/', LandingPageView.as_view(), name='landing_page'),
    
    # Authentication paths
    path('login/', CustomLoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    
    # Custom password reset views
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    
    # Default Django auth views for password reset process
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # Dashboard and additional paths
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    
    # Game views
    path('levels/', views.levels, name='levels'),
    path('level1/', views.level1, name='level1'),
    path('level2/', views.level2, name='level2'),
    path('level3/', views.level3, name='level3'),
]










