SHELL := cmd.exe

run:
	venv\Scripts\activate && uvicorn --reload api.routes.base:app

configure: venv
	venv\Scripts\activate && pip install -r requirements.dev.txt -r requirements.txt

venv:
	python -m venv venv

format:
	venv\Scripts\activate && autoflake -r --in-place --remove-all-unused-imports ./api
	venv\Scripts\activate && isort ./api
	venv\Scripts\activate && black ./api
	venv\Scripts\activate && autoflake -r --in-place --remove-all-unused-imports ./migrations
	venv\Scripts\activate && isort ./migrations
	venv\Scripts\activate && black ./migrations

db:
	docker run -d -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust --name western_prep_dp postgres:15

migrate:
	venv\Scripts\activate && alembic upgrade head