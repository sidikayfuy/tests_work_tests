from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User


class Test(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.CharField(max_length=250)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class Answer(models.Model):
    text = models.CharField(max_length=250)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    right = models.BooleanField()

    def __str__(self):
        return self.text


class Result(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answers = models.CharField(max_length=250)
    percent = models.FloatField(null=True)

    def __str__(self):
        return f"{self.test.title} {self.user.username} {self.percent}"

