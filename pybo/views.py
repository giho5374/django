from django.shortcuts import render, get_object_or_404,redirect # 404일 경우 ,페이지 이동
from django.http import HttpResponse # http의 응답
from .models import Question
from django.utils import timezone
# Create your views here.
# 응답 꾸러미들

def index(request):
    '''
    pybo 목록 출력
    '''
    question_list = Question.objects.order_by('-create_date') # -로 역순
    context = {'question_list':question_list}
    # return HttpResponse('Hi pybo') # Hi pybo를 response해라
    return render(request,'pybo/question_list.html',context)

def detail(request,question_id):
    '''
    pybo 내용 출력
    '''
    # question = Question.objects.get(id = question_id)
    question = get_object_or_404(Question,pk=question_id)
    context = {'question':question}
    return render(request,'pybo/question_detail.html',context)

def answer_create(request,question_id):
    '''
    pybo 답변 등록
    '''
    question = get_object_or_404(Question,pk=question_id)
    question.answer_set.create(content = request.POST.get('content'),
                               create_date = timezone.now())
    return redirect('pybo:detail',question_id=question_id)