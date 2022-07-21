from django.utils.text import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class GameTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Assignee : 훈희

    jwt token에서 같이 서빙되는 claim을 custom

    """

    @classmethod
    def get_token(cls, user):
        """생성된 토큰 가져오기"""
        token = super().get_token(user)

        """사용자 지정 클레임 설정하기"""
        token["id"] = user.id
        token["email"] = user.email

        return token


class RefreshTokenSerializer(serializers.Serializer):
    """
    Assignee : 훈희

    로그아웃시 토큰 반납을 위한 시리얼라이저입니다.

    """

    refresh = serializers.CharField()

    default_error_messages = {"bad_token": _("Token is invalid or expired")}

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad_token")
