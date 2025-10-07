from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .api_views import (
    CustomTokenObtainPairView,
    register_user,
    logout_user,
    user_profile,
    verify_token
)

urlpatterns = [
    # Endpoints JWT estándar
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Endpoints personalizados
    path('register/', register_user, name='api_register'),
    path('logout/', logout_user, name='api_logout'),
    path('profile/', user_profile, name='api_profile'),
    path('verify/', verify_token, name='api_verify_token'),
]
