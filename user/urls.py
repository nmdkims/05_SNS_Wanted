from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import LoginView, LogoutView, UserSignupApiView

urlpatterns = [
    path("api/token", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup", UserSignupApiView.as_view()),
    path("login", LoginView.as_view()),
    path("logout", LogoutView.as_view()),
]
