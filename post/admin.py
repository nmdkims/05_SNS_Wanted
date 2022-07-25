from django.contrib import admin

from post.models import Post as PostModel
from post.models import Status as StatusModel


class PostModelAdmin(admin.ModelAdmin):
    """
    Assignee : 훈희
    Post 모델을 어드민 사이트에 설정합니다.
    """

    list_display = ("id", "writer", "title", "content", "created_at", "updated_at")


admin.site.register(PostModel, PostModelAdmin)


class StatusModelAdmin(admin.ModelAdmin):
    """
    Assignee : 훈희
    Status 모델을 어드민 사이트에 설정합니다.
    """

    list_display = ("id", "status")


admin.site.register(StatusModel, StatusModelAdmin)
