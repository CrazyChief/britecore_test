.PHONY: requirements

# Set environment variables
ENVIRONMENT = set -o allexport; . ./.env; set +o allexport;

# Set the following variable to you project name
PROJECT_NAME = britecore_test
DEFAULT_VIRTUALENV = .venv
# Possible virtualenv if virtualenvwrapper is used
POSSIBLE_VIRTUALENV = $(VIRTUAL_ENV)
# Use possible virtualenv if it exists and virtualenvwrapper is used, otherwise use default one
VIRTUALENV = $(if $(wildcard $(POSSIBLE_VIRTUALENV)),$(POSSIBLE_VIRTUALENV),$(DEFAULT_VIRTUALENV))

PYVERSION=3.6
PIP = $(VIRTUALENV)/bin/pip
PYTHON = $(VIRTUALENV)/bin/python
PYTEST = $(VIRTUALENV)/bin/pytest

app=
apps=

venv:
	@echo "Creating virtual environment within \"$(VIRTUALENV)\" directory"
	@python$(PYVERSION) -m venv $(VIRTUALENV) || rm -rf $(VIRTUALENV) && virtualenv -p `which python$(PYVERSION)` $(VIRTUALENV)

environment:
	@echo "Local environment preparation"
	@cp .env.example .env
	@echo "Do not forget to edit it at $(shell pwd)/.env"

requirements:
	@echo "Installing $(PROJECT_NAME) requirements"
	@$(PIP) install -qr requirements.txt

collectstatic:
	@echo "Collecting static files for Django site"
	@$(ENVIRONMENT)$(PYTHON) $(PROJECT_NAME)/manage.py collectstatic -v 0 --noinput

run:
	@$(ENVIRONMENT)$(PYTHON) $(PROJECT_NAME)/manage.py runserver $(host)

dev_run:
	@$(ENVIRONMENT)$(PYTHON) $(PROJECT_NAME)/manage.py runserver 0.0.0.0:8123

shell:
	@$(ENVIRONMENT)$(PYTHON) $(PROJECT_NAME)/manage.py shell

dbshell:
	@$(ENVIRONMENT)$(PYTHON) $(PROJECT_NAME)/manage.py dbshell

migrations:
	@echo "Generating migrations"
	@$(ENVIRONMENT)$(PYTHON) $(PROJECT_NAME)/manage.py makemigrations $(apps)

migrate:
	@echo "Applying migrations"
	@$(ENVIRONMENT)$(PYTHON) $(PROJECT_NAME)/manage.py migrate -v 0 --noinput $(app)

superuser:
	@$(ENVIRONMENT)$(PYTHON) $(PROJECT_NAME)/manage.py createsuperuser

clean:
	@echo "Cleaning __pycache__ directories"
	@find . -name "__pycache__" -exec rm -rf {} 2> /dev/null \; 2> /dev/null || true

test:
	@$(ENVIRONMENT)$(PYTEST) -sx --pep8 $(PROJECT_NAME)/$(app) || true

serve:
	@echo "Start serving frontend..."
	@yarn --cwd frontend/ serve

build:
	@echo "Start building frontend..."
	@yarn --cwd frontend/ build
