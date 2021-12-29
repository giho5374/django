from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Question(models.Model):
    subject = models.CharField(max_length=200) # 글자 수 제한하려면 charField
    content = models.TextField() # 글자수 제한 X
    create_date = models.DateTimeField() # 시간
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self): # Question.objects.all에 보기 편한 format
        return self.subject

class Answer(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE) # 질문에 대한 답변이므로 foreinkey , 질문과 함께 삭제
    content = models.TextField()
    create_date = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)