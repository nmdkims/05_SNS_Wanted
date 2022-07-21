from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from user.jwt_claim_serializer import (GameTokenObtainPairSerializer,
                                       RefreshTokenSerializer)
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
        "email" : "test1@gmail.com",
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


# /users/logout
class LogoutView(GenericAPIView):
    """
     Assignee : 훈희

     post : 로그아웃
     로그아웃 하면서 토큰을 같이 반납합니다.
     기존의 delete method를 사용하지 않으며 post 방식으로 refresh token을
     보내주게 됩니다.

     로그인시 입력 data 타입 json 구조는 밑과 같습니다.
    {
       "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY1NzkwMzY5MywiaWF0IjoxNjU3ODE3MjkzLCJqdGkiOiJkMjdiMGUxNDU1NTc0NWRjYWRiOTU4YzA1YjA4ZGEzNiIsInVzZXJfaWQiOjgsImlkIjo4LCJuaWNrbmFtZSI6InRlc3Q0MiJ9.iqLPbGoFxaFbp0yXvsKjBwgT7EF29I6URi7O05j2YVg"
    }

    """

    serializer_class = RefreshTokenSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args):
        refresh = self.get_serializer(data=request.data)
        refresh.is_valid(raise_exception=True)
        refresh.save()

        user = request.user
        logout(request)

        return Response(
            f"user :{user} 로그아웃 성공!!, 토큰을 반납", status=status.HTTP_204_NO_CONTENT
        )
