from django.urls import path
from . import views

app_name = 'pybo' # pybo의 namespace

urlpatterns = [
    # path('',views.index),
    # path('<int:question_id>/', views.detail),  # 가변적인 endpoint, question.id의 타입은 int이다.
    path('',views.index, name = 'index'),
    path('<int:question_id>/', views.detail,name = 'detail'),
    path('answer/create/<int:question_id>/',views.answer_create,name = 'answer_create'),
    path('question/create/', views.question_create,name = 'question_create'),
]

