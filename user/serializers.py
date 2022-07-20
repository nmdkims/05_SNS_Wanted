from rest_framework import serializers

from user.models import User as UserModel


class UserSignupSerializer(serializers.ModelSerializer):
    """
    Assignee : 훈희

    회원가입 serializer 입니다.
    email에 대한 유효성 검사 password에 대한 유효성 검사를 수행
    create와 update를 지원합니다.

    """

    class Meta:
        model = UserModel
        fields = ["email", "password"]

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate(self, data):
        if data.get("email"):
            if not len(data.get("email", "")) >= 6:
                raise serializers.ValidationError(
                    detail={"error": "email의 길이는 6자리 이상이어야 합니다."}
                )

        if not len(data.get("password", "")) >= 6:
            raise serializers.ValidationError(
                detail={"error": "password의 길이는 6자리 이상이어야 합니다."}
            )

        return data

    def create(self, validated_data):
        password = validated_data.pop("password", "")

        user = UserModel(**validated_data)

        """ pbkdf2 알고리즘 방식으로 비밀번호 암호화 """
        user.set_password(password)
        user.save()

        return user

    def update(self, instance, validated_data):

        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
                continue
            setattr(instance, key, value)
        instance.save()

        return instance


class UserSigninSerializer(serializers.ModelSerializer):
    """
    Assignee : 훈희

    로그인 serializer 입니다.

    """

    class Meta:
        model = UserModel
        fields = ["id", "email"]
