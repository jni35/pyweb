from django.urls import path
from polls import views
#네임 스페이스
app_name = 'poll'  #app_name변수에 poll앱 저장

urlpatterns = [
    path('', views.poll_list, name='index'), # 127.0.0.1:8000/poll/
    path('<int:pk>/', views.detail, name='detail'),
    path('<int:pk>/vote/', views.vote, name='vote'),
]