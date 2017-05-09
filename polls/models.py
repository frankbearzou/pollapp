from datetime import timedelta
from django.db import models
from django.db.models import F
from django.utils import timezone

# Create your models here.


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return (timezone.now() > self.pub_date) and (timezone.now() - self.pub_date <= timedelta(days=1))

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def vote(self):
        self.votes = F('votes') + 1
        self.save()

    def __str__(self):
        return self.choice_text
