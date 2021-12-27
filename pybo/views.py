from django.shortcuts import render, get_object_or_404,redirect # 404일 경우 ,페이지 이동
from django.http import HttpResponse # http의 응답
from .models import Question
from django.utils import timezone
from .forms import QuestionForm,AnswerForm
from django.core.paginator import Paginator
# Create your views here.
# 응답 꾸러미들

def index(request):
    '''
    pybo 목록 출력
    '''
    page = request.GET.get('page',1)  # 페이지 / GET방식으로 page를 파라미터로 가져올 때 사용, 파라미터 없이 들어올 때 dafault값을 1로 줌.

    # 조회
    question_list = Question.objects.order_by('-create_date') # -로 역순

    # 페이징
    paginator = Paginator(question_list,10)  # 한 페이지당 개수
    page_obj = paginator.get_page(page)

    context = {'question_list':page_obj}
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
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id = question_id)
    else:
        form = AnswerForm()
    context = {'question':question, 'form':form}
    return render(request, 'pybo/question_detail.html', context)

def question_create(request):
    '''
    pybo 질문 등록
    '''
    if request.method =='POST':
        form = QuestionForm(request.POST)
        if form.is_valid(): # form이 유효한지 검증
            question = form.save(commit=False)  # form에 create_date이 없으므로 여기서 저장하면 에러발생!
            question.create_date = timezone.now()  # create_date를 넣어주고 저장
            question.save()
            return redirect('pybo:index')  # index는 초기화면이다
    else:
        form = QuestionForm()            # method가 GET인 경우
    context = {'form':form}
    return render(request,'pybo/question_form.html',context)