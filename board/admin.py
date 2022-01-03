from django.contrib import admin
from board.models import Question, Answer, Comment

admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Comment)

