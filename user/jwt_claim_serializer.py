from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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
        token["nickname"] = user.nickname

        return token
