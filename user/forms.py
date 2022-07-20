from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import User


class UserCreationForm(forms.ModelForm):
    """
    Assignee : 훈희

    BaseUserAdmin의 UserCreationForm을 오버라이딩 하기 위함

    custom 유저 모델을 이용하여 admin에서 유저를 생성하기
    위하여 작성 되어야 하는 form입니다.
    password1과 password2를 가지고 있으며 유저 모델에 정의한
    email을 가지고 있습니다.

    clean_password2 이용하여 password1과 password2가 일치하는지 검증합니다.

    마지막으로 def save를 통해 데이터를 저장합니다.

    """

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
    Assignee : 훈희

    BaseUserAdmin의 UserChangeForm 오버라이딩 하기 위함

    사용자 암호를 ReadOnlyPasswordHashField() 가져와서 화면에 표시할
    예정이며 해당 내용은 확인만 가능합니다.
    마지막에 저장할때 clean_password를 통해 password를 그대로 다시 저장합니다.

    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ("email", "password", "is_active", "is_admin")

    def clean_password(self):
        return self.initial["password"]
