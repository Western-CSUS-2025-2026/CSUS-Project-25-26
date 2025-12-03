SHELL := cmd.exe

run:
	venv\Scripts\activate && uvicorn --reload api.routes.base:app

configure: venv
	venv\Scripts\activate && pip install -r requirements.dev.txt -r requirements.txt

venv:
	python -m venv venv

format:
	source ./venv/bin/activate && autoflake -r --in-place --remove-all-unused-imports ./api
	source ./venv/bin/activate && isort ./api
	source ./venv/bin/activate && black ./api
	source ./venv/bin/activate && autoflake -r --in-place --remove-all-unused-imports ./migrations
	source ./venv/bin/activate && isort ./migrations
	source ./venv/bin/activate && black ./migrations
	
db:
	docker run -d -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust --name western_prep_db postgres:15

migrate:
	source ./venv/bin/activate && alembic upgrade head
