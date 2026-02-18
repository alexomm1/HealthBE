from django.db import models
from users.models import User


class Test(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

class Factor(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="factor")
    name = models.CharField(max_length=200)

class Results(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="results")
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, related_name="results")
    score = models.IntegerField(default=0)







class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=400)

class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

