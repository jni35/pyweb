from django import forms
from board.models import Question, Answer, Comment

#질문 등록폼
class QuestionForm(forms.ModelForm):
    class Meta:     #내부클래스, 중첩클래스
        model = Question
        fields = ['subject', 'content']
        labels = {
            'subject':'제목',
            'content':'내용'
        }

# 답변 등록폼
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {'content':'내용'}

# 댓글 등록폼
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {'content':'댓글 내용'}
