from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.jwt_claim_serializer import GameTokenObtainPairSerializer
from user.serializers import UserSigninSerializer, UserSignupSerializer


# /users/signup
class UserSignupApiView(APIView):
    """
    Assignee : 훈희

    post : 회원가입
    회원가입시 입력 data 타입 json 구조는 밑과 같습니다.
    {
        "email" : "test1@gmail.com",
        "password" : "root1234"
    }
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"messages": "가입 성공"}, status=status.HTTP_200_OK)
        else:
            return Response({"messages": "가입 실패"}, status=status.HTTP_400_BAD_REQUEST)


# /users/login
class LoginView(APIView):
    """
    Assignee : 훈희

    post : 로그인
    로그인 할때 access token과 refresh token을 함께 가져옴

    로그인시 입력 data 타입 json 구조는 밑과 같습니다.
    {
        "email" : "test1",
        "password" : "root1234"
    }

    delete: 로그아웃

    """

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email", "")
        password = request.data.get("password", "")

        user = authenticate(request, username=email, password=password)
        if not user:
            return Response(
                {"error": "존재하지 않는 계정이거나 패스워드가 일치하지 않습니다."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        user_serializer = UserSigninSerializer(user)
        token = GameTokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)

        response = Response(
            {
                "user": user_serializer.data,
                "message": "로그인 성공!!",
                "token": {
                    "access": access_token,
                    "refresh": refresh_token,
                },
            },
            status=status.HTTP_200_OK,
        )
        login(request, user)
        return response

    def delete(self, request):
        user = request.user
        logout(request)
        return Response(f"user :{user} 로그아웃 성공!!, 토큰을 유지")
