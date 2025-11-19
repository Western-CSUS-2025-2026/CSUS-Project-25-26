SHELL := /bin/bash

run:
	source ./venv/bin/activate && uvicorn --reload api.routes.base:app

configure: venv
	source ./venv/bin/activate && pip install -r requirements.dev.txt -r requirements.txt

venv:
	python3.11 -m venv venv

format:
	autoflake -r --in-place --remove-all-unused-imports ./api
	isort ./api
	black ./api
	autoflake -r --in-place --remove-all-unused-imports ./migrations
	isort ./migrations
	black ./migrations
	
db:
	docker run -d -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust --name western_prep_dp postgres:15

migrate:
	source ./venv/bin/activate && alembic upgrade head
