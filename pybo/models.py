from django.db import models
from django.contrib.auth.models import User  # 회원가입 모델


# Create your models here.

class Question(models.Model):
    subject = models.CharField(max_length=200)  # 글자 수 제한하려면 charField
    content = models.TextField()  # 글자수 제한 X
    create_date = models.DateTimeField()  # 시간
    modify_date = models.DateTimeField(null=True, blank=True)  # blank = True 로 form.is_valid에서 오류 X
    author = models.ForeignKey(User, on_delete=models.CASCADE,  # 작성자는 User를 외래키로 받음.
                               related_name='author_question')
    voter = models.ManyToManyField(User, related_name='voter_question')

    def __str__(self):  # Question.objects.all에 보기 편한 format
        return self.subject


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)  # 질문에 대한 답변이므로 foreinkey , 질문과 함께 삭제
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_answer')
    voter = models.ManyToManyField(User, related_name='voter_answer')


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    create_date = models.DateTimeField()
    modify_date = models.DateTimeField(null=True, blank=True)
    question = models.ForeignKey(Question, null=True, blank=True, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, null=True, blank=True, on_delete=models.CASCADE)
