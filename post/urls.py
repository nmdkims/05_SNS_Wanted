from django.urls import path

from .views import PostView

urlpatterns = [
    path("v1/posts", PostView.as_view()),
]
