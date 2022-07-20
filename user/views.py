from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from user.serializers import UserSignupSerializer


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
