# Проект api_yamdb
### Описание
YaMDb - проект, который собирает отзывы пользователей на произведения. Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку. Произведения делятся на следующие категории категории: «Книги», «Фильмы», «Музыка». При необходимости список категорий может быть расширен. Добавлять произведения, категории и жанры может только администратор. Пользователи могут оставлять к произведениям текстовые отзывы и ставить оценку.

### Стек технологий

    Python 3.9,
    Django 2.2,
    DRF

### Установка
Клонировать репозиторий и перейти в него в командной строке.
Установить и активировать виртуальное окружение c учетом версии Python 3.9:

    python -m venv venv

    source venv/Scripts/activate

Установить все зависимости из файла requirements.txt

    pip install -r requirements.txt

Выполнить миграции:

    python manage.py migrate

Создать суперпользователя:

    python manage.py createsuperuser

Запуск проекта:

    python manage.py runserver

### Примеры запросов к API

Регистрация нового пользователя:

    POST /auth/signup/
    в body
    {
    "email": "user@example.com",
    "username": "string"
    }
    
Пример ответа:

    {
    "email": "string"
    "username": "string"
    }
    
Получение списка всех категорий:

    GET /categories

Пример ответа:

    {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
        {...}
      ]
    }
    
Удаление жанра:

    DELETE /genres/{slug}/
    
Добавление произведения:

    POST /titles
    в body
    {
    "name": "string",
    "year": 0,
    "description": "string",
    "genre": [
        "string"
      ],
    "catigory": 'string"
    }

Частичное обновлние отзыва:

    PATCH /titles/{title_id}/reviews/{review_id}
    в body
    {
    "text": "string",
    "score": 1
    }
    
Пример ответа:

    {
    "id": 0,
    "text": "string",
    "author": "string",
    "score": 1,
    "pub_date": "2019-08-24T14:15:22Z"
    }
    
Получение списка пользователей:

    GET /users/
    
Привер ответа:

    {
    "count": 0,
    "next": "string",
    "previous": "string",
    "resilts": [
        {...}
      ]
    }
    
Более подробно про все команды можно узнать из документации, доступной после запуска проекта по адресу http://127.0.0.1:8000/redoc/

Авторы:
- [Алексей Мещеряков](https://github.com/Luohins)
- [Вадим Барнёв](https://github.com/acktor76)
- [Сергей Лазарь](https://github.com/SergeiLazar)
