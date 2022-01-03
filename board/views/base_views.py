from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from board.models import Question, Answer, Comment
from board.forms import QuestionForm, AnswerForm, CommentForm

def index(request):
    return render(request, 'board/index.html')

def boardlist(request):

    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')

    #조회
    question_list = Question.objects.order_by('-create_date')
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |
            Q(content__icontains=kw) |
            Q(author__username__icontains=kw) | #질문 글쓴이
            Q(answer__author__username__icontains=kw) |   #답변 글쓴이
            Q(answer__content__icontains=kw)
        ).distinct() #유일한 것 검색

    #페이징 처리
    paginator = Paginator(question_list, 10)
    page_obj = paginator.get_page(page)
    context = {'question_list':page_obj, 'page':page, 'kw':kw}
    return render(request, 'board/question_list.html',context)


def detail(request, question_id):
    # 질문/답변 상세
    # question = Question.objects.get(id=question_id) #해당 id의 질문
    question = get_object_or_404(Question, pk=question_id)
    #경로에 오류가 있을 때 404로 처리(페이지가 없음)
    return render(request, 'board/detail.html', {'question':question})