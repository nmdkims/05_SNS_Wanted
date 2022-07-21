from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import UserChangeForm, UserCreationForm
from .models import User


class UserAdmin(BaseUserAdmin):
    """
    Assignee : 훈희

    Custom된 유저 모델 사용을 위한 admin Custom
    form과 사용자 add_form을 custom한 폼을 이용한 것으로 변경

    장고에서 기본으로 제공하는 Group은 사용하지 않도록 설정

    """

    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ("id", "email", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_admin",)}),
    )

    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),)
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
