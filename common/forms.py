from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm): # 이 폼은 username,password1,password2를 속성으로 가지고있음
    email = forms.EmailField(label='이메일') # 추가한것

    class Meta:
        model = User
        fields = ("username",'email')