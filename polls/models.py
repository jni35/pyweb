from django.db import models

# Question 모델(Model을 상속받음) - 테이블과 같은 의미
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField()

    def __str__(self):  #질문 내용이 문자로 출력됨
        return self.question_text

# Choice 모델
class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE) #외래키

    def __str__(self):
        return self.choice_text
