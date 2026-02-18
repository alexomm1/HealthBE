from django.contrib import admin
from .models import Test, Factor, TestResults, TestAttempts

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(Factor)
class FactorAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(TestResults)
class ResultsAdmin(admin.ModelAdmin):
    list_display = ['user', 'score']

@admin.register(TestAttempts)
class TestAttemptsAdmin(admin.ModelAdmin):
    list_display =  ['id', 'user']
