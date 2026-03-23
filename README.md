# API для Yatube

REST API для социальной сети Yatube. Проект позволяет управлять публикациями, комментариями, сообществами и подписками через HTTP-запросы. Реализована система аутентификации с использованием JWT-токенов, права доступа для авторов контента и пагинация выдачи данных.

## Технологии

- Python 3.12
- Django 4.2+
- Django REST Framework
- Djoser
- djangorestframework-simplejwt
- django-filter

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone <ссылка_на_репозиторий>
   cd api_final_yatube

2. Создайте и активируйте виртуальное окружение:
    python -m venv venv
    # Для Windows:
    venv\Scripts\activate
    # Для macOS/Linux:
    source venv/bin/activate

3. Установите зависимости:
    pip install -r requirements.txt

4. Выполните миграции базы данных:
    python manage.py migrate

5. Запустите проект:
    python manage.py runserver

6. API будет доступно по адресу: http://127.0.0.1:8000/api/v1/


Документация (ReDoc): http://127.0.0.1:8000/redoc/
Примеры запросов к API
Для авторизованных запросов необходимо передавать токен в заголовке:
Authorization: Bearer <ваш_токен>

1. Получение токена
    POST /api/v1/jwt/create/
    {
      "username": "myuser",
      "password": "secure_password"
    }

2. Создание публикации
    POST /api/v1/posts/
    Заголовок: Authorization: Bearer <access_token>
    {
      "text": "Моя первая публикация!",
      "group": 1
    }

3. Получение списка публикаций (с пагинацией)
    GET /api/v1/posts/?limit=2&offset=0
    Ответ:
    {
      "count": 10,
      "next": "http://127.0.0.1:8000/api/v1/posts/?limit=2&offset=2",
      "previous": null,
      "results": [
        {
            "id": 1,
            "text": "Моя первая публикация!",
            "author": "myuser",
            "pub_date": "2023-10-25T12:00:00Z",
            "group": 1
        }
      ]
    }

4. Добавление комментария
    POST /api/v1/posts/1/comments/
    Заголовок: Authorization: Bearer <access_token>
    {
      "text": "Отличный пост!"
    }

5. Подписка на пользователя
    POST /api/v1/follow/
    Заголовок: Authorization: Bearer <access_token>
    {
      following": "another_user"
    }

6. Поиск в подписках
    GET /api/v1/follow/?search=alex
    Возвращает только тех пользователей, на которых вы подписаны и чье имя содержит "alex".
    ```