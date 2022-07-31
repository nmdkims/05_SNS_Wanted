from django.core.paginator import Paginator
from django.db.models import Count, Q
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from post.models import Post as PostModel
from post.serializers import PostListSerializer, PostSerializer


# url : /api/posts
class PostView(APIView):
    """
    Assignee : 훈희

    게시글 목록 생성, 조회를 위한 view입니다.
    GET : 게시글 상세 조회
    POST : 게시글 생성

    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Assignee : 훈희
        게시글 상세 조회합니다.
        """

        posts = PostModel.objects.all()
        serializer = PostListSerializer(posts, many=True)

        """게시글 정렬 기능"""
        sort = request.GET.get("sort", "")
        if sort == "asc":
            posts = posts.order_by("created_at")
        elif sort == "desc":
            posts = posts.order_by("-created_at")
        elif sort == "likes1":
            posts = posts.annotate(like=Count("likes__user_like")).order_by("like", "id")
        elif sort == "likes2":
            posts = posts.annotate(like=Count("likes__user_like")).order_by("-like", "-id")
        elif sort == "views1":
            posts = posts.order_by("views", "id")
        elif sort == "views2":
            posts = posts.order_by("-views", "-id")

        """키워드 검색 기능"""
        search_keyword = request.GET.get("search")
        if search_keyword:
            posts = posts.filter(Q(is_deleted=False) & Q(title__icontains=search_keyword))

        """필터링 기능"""
        hashtags = request.GET.get("hashtags")
        if hashtags:
            posts = posts.filter(Q(is_deleted=False) & Q(hashtags__icontains=hashtags))

        """pagination 기능"""
        page_number = self.request.query_params.get("page", 1)
        page_size = self.request.query_params.get("page_count", 10)
        paginator = Paginator(posts, page_size)
        serializer = serializer(paginator.page(page_number), many=True, context={"request": request})

        if not posts:
            return Response({"error": "게시글이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)

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


class PostDetailView(APIView):
    """
    Assignee: 훈희

    query param: post_id
    return: json
    detail:
      - 인증/인가에 통과한 유저는 모든 게시글을 조회할 수 있습니다.(GET: 게시글 상세 조회 기능)
      - 인증/인가에 통과한 유저는 본인의 게시글을 수정할 수 있습니다.(PATCH: 게시글 수정 기능)
      - 인증/인가에 통과한 유저는 본인의 게시글을 삭제할 수 있습니다.(DELETE: 게시글 삭제 기능)
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, post_id):
        """
        GET: 게시글 조회(상세) 기능[조회수 증가]
        """
