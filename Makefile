.PHONY: run migrate test setup

setup:
	pip install -r requirements/local.txt

run:
	python manage.py runserver

migrate:
	python manage.py makemigrations
	python manage.py migrate

reset-demo:
	python manage.py reset_demo_data

admin:
	python manage.py ensure_admin

test:
	pytest

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
