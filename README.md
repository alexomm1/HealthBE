# Health BE — Система психологического тестирования

Backend на Django Rest Framework для обработки результатов тестов и ведения статистики.

## Запуск проекта

### 1. Установка окружения и зависимостей
Проект использует менеджер пакетов **uv**. Для установки виртуального окружения и всех библиотек выполните:

```
uv sync
```
### 2. Настройка переменных окружения
Создайте файл .env в директории mysite/ и добавьте в него следующие параметры:
```
DEBUG=True
SECRET_KEY=your_secret_key
GOOGLE_OAUTH2_KEY=your_google_oauth_key
GOOGLE_OAUTH2_SECRET=your_google_oauth_secret_key
```
### 3. Миграции базы данных
Подготовьте структуру таблиц перед первым запуском:

`uv run manage.py migrate`

### 4. Запуск сервера разработки
Запустите локальный сервер:

`uv run manage.py runserver`

### Тестирование
#### Запуск тестов сериализаторов
`uv run manage.py test tests.test_serializers`
#### Запуск всех тестов в папке tests
`uv run manage.py test tests`

### Технологии
Python 3.13 (uv)<br>
Django & DRF<br>
Google OAuth2