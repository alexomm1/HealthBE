from django.db import models
from users.models import User


class Test(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

class Factor(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="factor")
    name = models.CharField(max_length=200)

class TestAttempts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="attempts")
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name="attempts")
    completed_at = models.DateTimeField(auto_now_add=True)

class TestResults(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="results")
    attempt = models.ForeignKey(TestAttempts, on_delete=models.CASCADE, related_name="results")
    factor = models.ForeignKey(Factor, on_delete=models.CASCADE, related_name="results")
    score = models.IntegerField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)
