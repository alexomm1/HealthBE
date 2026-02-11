from django.contrib import admin
from .models import Test, Question, AnswerOption

admin.site.register(Test)
admin.site.register(Question)
admin.site.register(AnswerOption)