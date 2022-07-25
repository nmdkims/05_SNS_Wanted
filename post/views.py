from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from post.serializers import PostSerializer


# url : /api/posts
class PostView(APIView):
    """
    Assignee : 훈희

    게시글 목록 생성, 조회를 위한 view입니다.
    GET : 게시글 목록 조회
    POST : 게시글 생성

    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        게시글 생성
        필드에 writer를 넣어주긴하지만 해당내용은 writer의 id가 들어가기 때문에 request.user를
        context에 넣어서 시리얼라이저에 전달 합니다.

        """
        serializer = PostSerializer(data=request.data, context={"user": request.user})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "게시글 작성 성공"}, status=status.HTTP_201_CREATED)
