# Планировщик задач (Task Planner)
## Приложение для планирования задач и целей.

Студент: Михайлов Александр

____

### Cтек технологий используемых в приложении:

- **Python 3.11**
- **Django 4.2**
- **Flake8**
- **Postgres SQL**
- **Docker**

____

### Структура приложения:

- **Директория core** - *Директория c кастомной моделью пользователя*

- **Директория todolist** - *Директория с основной django (backend) частью приложения*

**manage.py** - *файл со ссылкой на скрипт django-admin для проекта*

**docker-compose.yaml** - *файл конфигурации для Docker Compose*

**requirements.txt** - *зависимости приложения*

**.gitignore** - *файлы и папки для игнорирования в системе контроля версий Git*
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

- SECRET_KEY=your_secret_key 
- DEBUG=True 
- DB_NAME=postgres
- DB_PASSWORD=postgres
- DB_USER=postgres
- DB_HOST=localhost 
- DB_PORT=5432
