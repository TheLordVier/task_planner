# Task Planner
## Application for planning tasks and goals.

Project developed by: Mikhailov Alexander

____

### Stack of technologies used in the application:

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

### Application structure:

- **Directory bot** - *Directory with data for Telegram bot operation*

- **Directory core** - *Directory with custom user model*

- **Directory tests** - *Application test directory*

- **Directory todolist** - *The directory with the main django (backend) part of the application*

- **Directory deploy** - *Directory with configuration files for Docker Compose*

- **Directory goals** - *Directory with boards, categories, goals and comments*

**manage.py** - *file with a link to the django-admin script for the project*

**requirements.txt** - *application dependencies*

**Dockerfile** - *container image file*

**entrypoint.sh** - *executable for Dockerfile*

**.dockerignore** - *files and folders to ignore in Docker*

**.gitignore** - *files and folders to ignore in the Git version control system*

**swagger.json** - *swagger connected to the project*
____

### Preparing and launching the application:

1. **Clone the application**
 - in the terminal, type the command `git clone https://github.com/TheLordVier/task_planner.git`
2. **Create a virtual environment**
 - in the terminal, enter the command in the project directory `python -m venv venv`
3. **Install application dependencies**
 - в терминале вводим команду `pip install -r requirements.txt` 
4. **Create an .env file (an example .env file is shown below)**
 - create an .env file in the root of the project and write in it the values of the variables used
5. **File docker-compose.yaml**
 - create and fill in the file docker-compose.yaml or take a ready-made one from the project
 - in the terminal, type the command `docker-compose up -d` 
6. **Performing migrations**
 - in the terminal, type the command `./manage.py makemigrations`
 - then enter the command `./manage.py migrate`
 - check the performed migrations with the command `./manage.py showmigrations`
7. **Launch the application**
 - in the terminal, enter the command in the project root `./manage.py runserver`
 - go to http://127.0.0.1:8000/ or log in to the admin panel http://127.0.0.1:8000/admin/
8. **You can also use the application located in the Yandex Cloud at http://51.250.70.227/auth.**

____

### An example of filling out an .env file:

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