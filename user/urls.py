from django.urls import path

from user.views import UserSignupApiView, LoginView

urlpatterns = [
    path("signup", UserSignupApiView.as_view()),
    path("login", LoginView.as_view()),
]
