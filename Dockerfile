FROM python:3.11-slim
# Возможно надо будет поставить версию python 3.10 (docker images | grep python)

#ENV PIP_VERSION=23.1.2

RUN pip install --upgrade pip

WORKDIR /opt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#RUN apt-get update && apt-get install -y --no-install-recommends gcc

COPY requirements.txt .

RUN python3 -m pip install --no-cache -r requirements.txt

COPY . .

ENTRYPOINT ["bash", "entrypoint.sh"]

EXPOSE 8000

#CMD ["gunicorn", "todolist.wsgi", "-w", "4", "-b", "0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]