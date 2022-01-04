from django.shortcuts import render, get_object_or_404,redirect # 404일 경우 ,페이지 이동
from django.http import HttpResponse # http의 응답
from .models import Question,Answer,Comment
from django.utils import timezone
from .forms import QuestionForm,AnswerForm,CommentForm
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
@login_required(login_url='common:login')
def answer_create(request,question_id):
    '''
    pybo 답변 등록
    '''
    question = get_object_or_404(Question,pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id = question_id)
    else:
        form = AnswerForm()
    context = {'question':question, 'form':form}
    return render(request, 'pybo/question_detail.html', context)

@login_required(login_url='common:login')
def question_create(request):
    '''
    pybo 질문 등록
    '''
    if request.method =='POST':
        form = QuestionForm(request.POST)
        if form.is_valid(): # form이 유효한지 검증
            question = form.save(commit=False)  # form에 create_date이 없으므로 여기서 저장하면 에러발생!
            question.author = request.user
            question.create_date = timezone.now()  # create_date를 넣어주고 저장
            question.save()
            return redirect('pybo:index')  # index는 초기화면이다
    else:
        form = QuestionForm()            # method가 GET인 경우
    context = {'form':form}
    return render(request,'pybo/question_form.html',context)

@login_required(login_url='common:login')
def question_modify(request,question_id):
    '''
    질문 수정
    '''
    question = get_object_or_404(Question, pk = question_id)
    if request.user != question.author:
        messages.error(request,'수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=question_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST,instance=question)
        if form.is_valid():
            question = form.save(commit = False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('pybo:detail',question_id = question_id)
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

@login_required(login_url='common:login')
def answer_modify(request,answer_id):
    '''
    답변 수정
    '''
    answer = get_object_or_404(Answer, pk = answer_id)
    if request.user != answer.author:
        messages.error(request,'수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=answer.question.id)

    if request.method == 'POST':
        form = AnswerForm(request.POST,instance=answer)
        if form.is_valid():
            answer = form.save(commit = False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('pybo:detail',question_id = answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'form':form}
    return render(request,'pybo/answer_form.html',context)

@login_required(login_url='common:login')
def answer_delete(request,answer_id):
    '''
    답변 삭제
    '''
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=answer.question.id)
    else:
        answer.delete()
    return redirect('pybo:index')

@login_required(login_url='common:login')
def comment_create_question(request,question_id):
    '''
    pybo 질문 댓글 등록
    '''
    question = get_object_or_404(Question,pk=question_id)
    if request.method =='POST':
        form = CommentForm(request.POST)
        if form.is_valid(): # form이 유효한지 검증
            comment = form.save(commit=False)  # form에 create_date이 없으므로 여기서 저장하면 에러발생!
            comment.author = request.user
            comment.create_date = timezone.now()  # create_date를 넣어주고 저장
            comment.question = question
            comment.save()
            return redirect('pybo:detail',question_id = question_id)  # index는 초기화면이다
    else:
        form = CommentForm()            # method가 GET인 경우
    context = {'form':form}
    return render(request,'pybo/comment_form.html',context)

@login_required(login_url='common:login')
def comment_modify_question(request,comment_id):
    '''
    댓글 수정
    '''
    comment = get_object_or_404(Comment, pk = comment_id)
    if request.user != comment.author:
        messages.error(request,'수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=comment.question.id)

    if request.method == 'POST':
        form = CommentForm(request.POST,instance=comment)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail',question_id = comment.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form':form}
    return render(request,'pybo/comment_form.html',context)

@login_required(login_url='common:login')
def comment_delete_question(request,comment_id):
    '''
    댓글 삭제
    '''
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글 삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=comment.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id = comment.question.id)

@login_required(login_url='common:login')
def comment_create_answer(request,answer_id):
    '''
    답변 댓글 등록
    '''
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():  # form이 유효한지 검증
            comment = form.save(commit=False)  # form에 create_date이 없으므로 여기서 저장하면 에러발생!
            comment.author = request.user
            comment.create_date = timezone.now()  # create_date를 넣어주고 저장
            comment.answer = answer
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)  # index는 초기화면이다
    else:
        form = CommentForm()  # method가 GET인 경우
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_answer(request,comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('pybo:detail', question_id=comment.answer.question.id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'pybo/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_answer(request,comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글 삭제 권한이 없습니다.')
        return redirect('pybo:detail', question_id=comment.answer.question.id)
    else:
        comment.delete()
    return redirect('pybo:detail', question_id=comment.answer.question.id)