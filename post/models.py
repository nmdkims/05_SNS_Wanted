from django.db import models

from user.models import User as UserModel


class Hashtag(models.Model):
    hashtag = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.hashtag


class Status(models.Model):
    status = models.CharField("상태", max_length=20)


class Post(models.Model):
    """
    Assignee : 훈희

    게시글에 대한 모델입니다.
    작성자를 외래키로 참조하면서 해당 작성자가 삭제될시
    내용을 같이 처분합니다.

    유효성 검사 status를 이용한 soft delete구현을 생각합니다.
    유저가 게시물을 지운다고 하여도 상태를 변화 시킨 상태로 삭제를 한 것으로 만들어주고
    delete상태일때는 해당 게시물의 접근이나 수정이 되지 않는 상태로 합니다.

    hashtag는 범용성을 위하여 다른 모델로 빼놓은 구조입니다.

    작성시간과 수정시간이 표시 됩니다.

    """

    id = models.BigAutoField(primary_key=True)
    writer = models.ForeignKey(to=UserModel, verbose_name="작성자", on_delete=models.CASCADE, related_name="post_writer")
    title = models.CharField("제목", max_length=32)
    content = models.TextField("내용")
    status = models.ForeignKey(to=Status, verbose_name="상태", on_delete=models.CASCADE, related_name="post")

    hashtags = models.ManyToManyField(Hashtag, related_name="hashtag_articles", blank=True)

    created_at = models.DateTimeField("작성시간", auto_now_add=True)
    updated_at = models.DateTimeField("수정시간", auto_now=True)

    def __str__(self):
        return f"id : {self.id} / {self.writer}의 게시글"
