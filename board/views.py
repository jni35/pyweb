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

@login_required(login_url='common:login')
def question_create(request):
    #질문 등록
    if request.method == "POST":
        form = QuestionForm(request.POST)   #자료 전달받음(request.POST)
        if form.is_valid():
            question = form.save(commit=False) #가저장(날짜가 없어서 가저장)
            question.author = request.user
            question.create_date = timezone.now() #날짜 시간 저장
            question.save()  #실제 저장
            return redirect('board:index') #이동할 경로(앱 네임사용) 저장
    else:
        form = QuestionForm()   #form 객체 생성
    return render(request, 'board/question_form.html', {'form':form})

@login_required(login_url='common:login')
def answer_create(request, question_id):
    #답변 등록
    #question = Question.objects.get(id=question_id) #해당 id의 질문 객체 생성
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = AnswerForm(request.POST) #입력값 전달받음
        if form.is_valid():
            answer = form.save(commit=False)  #내용만 저장됨
            answer.author = request.user
            answer.create_date = timezone.now() #작성일
            answer.question = question  #외래키 질문 저장
            answer.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = AnswerForm()
    context = {'question':question,'form':form}
    return render(request, 'board/detail.html', context)

#질문 수정
@login_required(login_url='common:login')
def question_modify(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('board:detail', question_id=question.id)

    if request.method =="POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.modify_date = timezone.now()
            question.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = QuestionForm(instance=question)
    context = {'form':form}
    return render(request, 'board/question_form.html', context)

#질문 삭제
@login_required(login_url='common:login')
def question_delete(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('board:detail', question_id=question.id)
    question.delete()
    return redirect('board:index')

#답변수정
@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method =="POST":
        form = AnswerForm(request.POST, instance=answer)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.modify_date = timezone.now()
            answer.save()
            return redirect('board:detail', question_id=answer.question.id)
    else:
        form = AnswerForm(instance=answer)
    context = {'answer':answer, 'form':form}
    return render(request, 'board/answer_form.html', context)

#답변 삭제
@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    answer.delete()
    return redirect('board:detail', question_id=answer.question.id)

#질문 추천
@login_required(login_url='common:login')
def vote_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다.')
    else:
        question.voter.add(request.user)    #추천 추가(로그인한 사람)
    return redirect('board:detail', question_id=question.id)

#질문 답변
@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user   #세션 권한
            comment.create_date = timezone.now()
            comment.question = question     #참조권한
            comment.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = CommentForm()
    context = {'form':form}
    return render(request, 'board/comment_form.html', context)

#질문 댓글 삭제
@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    comment.delete()
    return redirect('board:detail', question_id=comment.question.id)\

#질문 댓글 수정
@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)  #변경된 입력 내용
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.modify_date = timezone.now()
            comment.save()
            return redirect('board:detail', question_id=comment.question.id)
    else:
        form = CommentForm(instance=comment)    #채워진 폼
    context = {'form':form}
    return render(request, 'board/comment_form.html', context)

