from django.contrib import admin
<<<<<<< feature/86c83t13e-save-test-result
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
=======
from .models import Test, Question, AnswerOption, Factor, Results

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(Factor)
class FactorAdmin(admin.ModelAdmin):
    list_display = ['name']

admin.site.register(Question)
admin.site.register(AnswerOption)


@admin.register(Results)
class ResultsAdmin(admin.ModelAdmin):
    list_display = ['user', 'get_test_title', 'get_factor_name', 'score']

    list_select_related = ['factor', 'user']

    @admin.display(description='Название фактора', ordering='factor__name')
    def get_factor_name(self, obj):
        return obj.factor.name

    @admin.display(description="Название теста", ordering='test__title')
    def get_test_title(self, obj):
        return obj.factor.test.title
>>>>>>> develop
