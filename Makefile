all: migrate start

start:
	@python manage.py runserver

migrate:
	@python manage.py makemigrations
	@python manage.py migrate

test:
	@pytest -s --pikachu -rA

coverage:
	@pytest --cov --pikachu