from django.contrib import admin
from .models import Test, Factor

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(Factor)
class FactorAdmin(admin.ModelAdmin):
    list_display = ['name']
