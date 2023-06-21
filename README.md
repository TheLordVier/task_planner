# Планировщик задач (Task Planner)
## Приложение для планирования задач и целей.

Проект разработал: Михайлов Александр

____

### Cтек технологий используемых в приложении:

- **Python 3.11**
- **Django 4.2**
- **Django REST framework 3.14.0**
- **Django-filter 23.2**
- **Social-auth-app-django 5.2.0**
- **Flake8**
- **Nginx-alpine**
- **Postgres SQL**
- **Docker, Docker-compose**
- **Telegram bot**
- **Pytest, Factory-boy**

____

### Структура приложения:

- **Директория bot** - *Директория c данными для работы Telegram бота*

- **Директория core** - *Директория c кастомной моделью пользователя*

- **Директория tests** - *Директория c тестами приложения*

- **Директория todolist** - *Директория с основной django (backend) частью приложения*

- **Директория deploy** - *Директория с файлами конфигурации для Docker Compose*

- **Директория goals** - *Директория c досками, категориями, целями и комментариями*

**manage.py** - *файл со ссылкой на скрипт django-admin для проекта*

**requirements.txt** - *зависимости приложения*

**Dockerfile** - *файл для создания образов контейнеров*

**entrypoint.sh** - *исполняемый файл для Dockerfile*

**.dockerignore** - *файлы и папки для игнорирования в Docker*

**.gitignore** - *файлы и папки для игнорирования в системе контроля версий Git*

**swagger.json** - *swagger подключённый к проекту*
____

### Подготовка и запуск приложения:

1. **Клонируем приложение.**
 - в терминале вводим команду `git clone https://github.com/TheLordVier/task_planner.git`
2. **Создаём виртуальное окружение.**
 - в терминале вводим команду в директории проекта `python -m venv venv`
3. **Устанавливаем зависимости приложения**
 - в терминале вводим команду `pip install -r requirements.txt` 
4. **Создаём .env файл (пример .env файла представлен ниже)**
 - создаём в корне проекта .env файл и прописываем в нём значения используемых переменных
5. **Файл docker-compose.yaml**
 - создаём и заполняем файл docker-compose.yaml или берём готовый из проекта
 - в терминале вводим команду `docker-compose up -d` 
6. **Выполняем миграции**
 - в терминале вводим команду `./manage.py makemigrations`
 - далее вводим команду `./manage.py migrate`
 - проверяем выполненные миграции с помощью команды `./manage.py showmigrations`
7. **Запускаем приложение**
 - в терминале вводим команду в корне проекта `./manage.py runserver`
 - переходим по пути http://127.0.0.1:8000/ или заходим в панель администратора http://127.0.0.1:8000/admin/

____

### Пример заполнения .env файла:

    SECRET_KEY=YOUR_SECRET_KEY
    DEBUG=True
    DB_NAME=postgres
    DB_PASSWORD=postgres
    DB_USER=postgres
    DB_HOST=localhost
    DB_PORT=5432
    SOCIAL_AUTH_VK_OAUTH2_KEY=YOUR_VK_APP_KEY
    SOCIAL_AUTH_VK_OAUTH2_SECRET=YOUR_VK_SECRET_KEY
    BOT_TOKEN=YOUR_SECRET_TELEGRAM_BOT_TOKEN
