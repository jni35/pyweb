from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from board.models import Question, Answer, Comment
from board.forms import QuestionForm, AnswerForm, CommentForm

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

