# Pre-Req:
# you should have activated the venv with this command:
# "source venv/bin/activate"

PROJECT=budget_management_system

.PHONY: setup-venv
setup-venv:
	python3 -m venv venv
	pip install -r requirements.txt


.PHONY: run
run:
	python manage.py runserver


.PHONY: migrate
migrate:
	python manage.py makemigrations
	python manage.py migrate


.PHONY: worker
worker:
	celery -A $(PROJECT) worker --loglevel=info


.PHONY: beat
beat:
	celery -A $(PROJECT) beat --loglevel=info


.PHONY: typecheck
typecheck:
	mypy core_app


.PHONY: format
format:
	black .
	isort .


.PHONY: lint
lint:
	flake8 core_app

.PHONY: test
test:
	docker-compose exec web pytest --ds=budget_management_system.settings