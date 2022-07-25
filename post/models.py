from django.db import models

from user.models import User as UserModel


class Post(models.Model):
    """
    Assignee : 희석

    사업장 별 가계부를 만들 수 있는 가계부 모델입니다.
    """

    id = models.BigAutoField(primary_key=True)
    writer = models.ForeignKey(to=UserModel, verbose_name="작성자", on_delete=models.CASCADE, related_name="post_writer")
    title = models.CharField("제목", max_length=32)
    content = models.TextField("내용")

    created_at = models.DateTimeField("작성시간", auto_now_add=True)
    updated_at = models.DateTimeField("수정시간", auto_now=True)

    def __str__(self):
        return f"id : {self.id} / {self.title}의 게시글"
