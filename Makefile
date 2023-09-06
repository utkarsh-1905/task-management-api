all: migrate start

start:
	@python manage.py runserver

migrate:
	@python manage.py makemigrations
	@python manage.py migrate

test:
	@coverage run -m pytest -s --pikachu

coverage:
	@coverage report -m
	@coverage html