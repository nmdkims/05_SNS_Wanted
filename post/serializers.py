from rest_framework import serializers

from post.models import Post as PostModel


class PostSerializer(serializers.ModelSerializer):
    """
    Assignee : 훈희
    게시글 등록을 위한 시리얼라이저입니다.
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
