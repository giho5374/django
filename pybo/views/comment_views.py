from django.shortcuts import render, get_object_or_404,redirect # 404일 경우 ,페이지 이동
from ..models import Question,Answer,Comment
from django.utils import timezone
from ..forms import CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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