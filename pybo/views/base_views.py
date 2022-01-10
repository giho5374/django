from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404
from ..models import Question
from django.db.models import Q

def index(request):  # 초기화면
    '''
    pybo 목록 출력
    '''
    page = request.GET.get('page', 1)  # 페이지 / GET방식으로 page를 파라미터로 가져올 때 사용, 파라미터 없이 들어올 때 dafault값을 1로 줌.
    kw = request.GET.get('kw','')  # 검색 / 없어도 됨
    # 조회
    question_list = Question.objects.order_by('-create_date')  # -로 역순
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) |
            Q(answer__author__username__icontains=kw)
        ).distinct()

    # 페이징
    paginator = Paginator(question_list,10)  # 한 페이지당 개수
    page_obj = paginator.get_page(page)  # html에 전달할 객

    context = {'question_list': page_obj, 'page': page, 'kw': kw}
    # return HttpResponse('Hi pybo') # Hi pybo를 response해라
    return render(request,'pybo/question_list.html',context)


def detail(request,question_id):  # 질문 상세 화면
    '''
    pybo 내용 출력
    '''
    # question = Question.objects.get(id = question_id)
    question = get_object_or_404(Question, pk=question_id)  # Qustion 모델에서 get으로 전달받은 question_id가 없으면 404 발생시킴
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
