from django.shortcuts import render, get_object_or_404,redirect # 404일 경우 ,페이지 이동
from ..models import Question
from django.utils import timezone
from ..forms import QuestionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


@login_required(login_url='common:login')
def question_create(request):  # 질문 작성
    '''
    pybo 질문 등록
    '''
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():  # form이 유효한지 검증 == 빈 값이 있는지 확인
            question = form.save(commit=False)  # form에 create_date이 없으므로 여기서 저장하면 에러발생!
            question.author = request.user
            question.create_date = timezone.now()  # create_date를 넣어주고 저장
            question.save()
            return redirect('pybo:index')  # index는 초기화면이다
    else:
        form = QuestionForm()            # method가 GET인 경우 미리 정의해둔 Question_Form을 전달
    context = {'form':form}
    return render(request,'pybo/question_form.html',context)


@login_required(login_url='common:login')
def question_modify(request,question_id):
    '''
    질문 수정
    '''
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST,instance=question)  # 수정시에 있는걸보니 QuestionForm에 question 안에 값을 그대로 넘겨주는 듯.
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail', question_id=question_id)
    else:
        form = QuestionForm(instance=question)
    context = {'form':form}
    return render(request,'pybo/question_form.html',context)

@login_required(login_url='common:login')
def question_delete(request,question_id):
    '''
    질문 삭제
    '''
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question_id)
    question.delete()
    return redirect('pybo:index')