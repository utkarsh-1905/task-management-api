FROM python:3.11-alpine

ENV PYTHONUNBUFFERED 1
ENV DEBUG False

WORKDIR /app

COPY . .

RUN python -m pip install -r requirements.txt
RUN python manage.py makemigrations user tasks project
RUN python manage.py migrate

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000