from django.urls import path
from board.views import base_views, question_views, answer_views, vote_views, comment_views

app_name = 'board'  #네임 스페이스 설정

urlpatterns = [
    #127.0.0.1:8000/board/
    #메인페이지
    path('', base_views.index, name='index'),
    #질문목록
    path('boardlist/', base_views.boardlist, name='boardlist'),
    #질문/답변 상세
    path('<int:question_id>/', base_views.detail, name='detail'),
    #질문 등록
    path('question/create/', question_views.question_create, name='question_create'),
    #질문 수정일
    path('question/modify/<int:question_id>/', question_views.question_modify, name='question_modify'),
    #질문 삭제
    path('question/delete/<int:question_id>/', question_views.question_delete, name='question_delete'),
    #답변 등록
    path('answer/create/<int:question_id>/', answer_views.answer_create, name='answer_create'),
    #답변 수정일
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'),
    #답변 삭제
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),
    #질문 추천
    path('vote/question/<int:question_id>/', vote_views.vote_question, name='vote_question'),
    #질문 댓글 등록
    path('comment/create/question/<int:question_id>/', comment_views.comment_create_question, name='comment_create_question'),
    #질문 댓글 삭제
    path('comment/delete/question/<int:comment_id>/', comment_views.comment_delete_question, name='comment_delete_question'),
    #질문 댓글 수정
    path('comment/modify/question/<int:comment_id>/', comment_views.comment_modify_question, name='comment_modify_question'),
]