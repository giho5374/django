from django import forms
from pybo.models import Question,Answer

class QuestionForm(forms.ModelForm): # forms.ModelForm을 상속받은 모델 폼
    class Meta: # 장고 모델폼은 Meta 내부 클래스를 반드시 포함해야함. 모델 폼이 사용할 모델과 필드를 작성.
        model = Question
        fields = ['subject','content']
        labels = {
            'subject':'제목',
            'content':'내용'
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content':'답변 내용',
        }