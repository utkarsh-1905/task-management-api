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

test-html:
	@pytest --html=report.html --self-contained-html --cov