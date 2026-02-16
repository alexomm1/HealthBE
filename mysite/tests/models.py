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


# . Таблица Тестов (tests)
# Хранит общую информацию о видах тестов.
# id (PK)
# name: "Шкала PSS 10", "Тест Бека" и т.д.
# description: Описание теста.
# 2. Таблица Факторов/Шкал (test_factors)
# Здесь мы описываем, какие именно показатели есть у конкретного теста.
# id (PK)
# test_id (FK -> tests.id)
# name: "Переживание стресса", "Контроль стресса", "Общий балл".
# key: Технический идентификатор (например, stress_experience), чтобы бэкенду было проще сопоставлять данные с мобилки.
# 3. Таблица Сессий Тестирования (test_sessions)
# Запись о том, что конкретный пользователь прошел конкретный тест в определенное время.
# id (PK)
# user_id (FK -> users.id)
# test_id (FK -> tests.id)
# completed_at: Дата и время завершения.
# 4. Таблица Результатов (test_results) — Самая важная
# Здесь хранятся те самые числовые значения.
# id (PK)
# session_id (FK -> test_sessions.id)
# factor_id (FK -> test_factors.id)
# score: Numeric/Float (твое числовое значение).