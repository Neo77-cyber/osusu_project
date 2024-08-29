# users/urls.py
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import UserRegistrationView, CustomTokenObtainPairView, ChangePasswordView


urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/register/', UserRegistrationView.as_view(), name='user-registration'),
    path('auth/change_password/', ChangePasswordView.as_view(), name='change_password'),
    
]
