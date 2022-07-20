from django.urls import path

from user.views import UserSignupApiView

urlpatterns = [
    path("signup", UserSignupApiView.as_view()),
]
