from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from board.models import Question, Answer, Comment
from board.forms import QuestionForm, AnswerForm, CommentForm

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