from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from board.models import Question, Answer
from board.forms import QuestionForm, AnswerForm

def index(request):
    return render(request, 'board/index.html')

def boardlist(request):
    #질문 목록
    #question_list = Question.objects.all()  #db 전체조회
    question_list = Question.objects.order_by('-create_date')
    #페이징 처리
    page = request.GET.get('page', 1)   #기본 1페이지
    paginator = Paginator(question_list, 10)    #페이지당 10개씩 설정
    page_obj = paginator.get_page(page)
    #작성일 기준 내림차순(- 기호 사용)
    return render(request, 'board/question_list.html', {'question_list':page_obj})
    #return HttpResponse("pyweb 사이트 입니다.")

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

