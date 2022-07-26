from rest_framework import serializers

from post.models import Post as PostModel


class PostSerializer(serializers.ModelSerializer):
    """
    Assignee : 훈희
    게시글 등록 시리얼라이저입니다.
    """

    class Meta:
        model = PostModel
        fields = [
            "status",
            "writer",
            "title",
            "content",
        ]

    def validate(self, data):
        if data["status"].status == "delete":  # public, private 만 가능
            raise serializers.ValidationError("잘못된 입력입니다.")
        return data

    def create(self, validated_data):
        """
        self.context["user"] : request.user
        """
        instance = PostModel(**validated_data)
        instance.user = self.context["user"]
        instance.save()
        return instance


class PostListSerializer(serializers.ModelSerializer):
    """
    Assignee : 훈희
    게시글 목록 조회 시리얼라이저입니다.
    """

    """ SerializerMethodField 이용해서 각각의 테이블을 특정하고 해당 외래키 연결된 곳의 필드에 접근 """
    writer = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_writer(self, obj):
        return obj.writer.email

    def get_status(self, obj):
        return obj.status.status

    class Meta:
        model = PostModel
        fields = [
            "id",
            "writer",
            "title",
            "content",
            "status",
            "hashtags",
        ]
