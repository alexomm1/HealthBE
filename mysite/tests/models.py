from django.db import models

class Test(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="questions")
    text = models.CharField(max_length=400)

class AnswerOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)


