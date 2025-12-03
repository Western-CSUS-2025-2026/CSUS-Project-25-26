SHELL := cmd.exe

run:
	venv\Scripts\activate && uvicorn --reload api.routes.base:app

configure: venv
	venv\Scripts\activate && pip install -r requirements.dev.txt -r requirements.txt

venv:
	python -m venv venv

format:
<<<<<<< HEAD
	venv\Scripts\activate && autoflake -r --in-place --remove-all-unused-imports ./api
	venv\Scripts\activate && isort ./api
	venv\Scripts\activate && black ./api
	venv\Scripts\activate && autoflake -r --in-place --remove-all-unused-imports ./migrations
	venv\Scripts\activate && isort ./migrations
	venv\Scripts\activate && black ./migrations

=======
	source ./venv/bin/activate && autoflake -r --in-place --remove-all-unused-imports ./api
	source ./venv/bin/activate && isort ./api
	source ./venv/bin/activate && black ./api
	source ./venv/bin/activate && autoflake -r --in-place --remove-all-unused-imports ./migrations
	source ./venv/bin/activate && isort ./migrations
	source ./venv/bin/activate && black ./migrations
	
>>>>>>> 5b0bc22330283a4f5cbe9a6efb3e49e2e3bde92d
db:
	docker run -d -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust --name western_prep_db postgres:15

migrate:
<<<<<<< HEAD
	venv\Scripts\activate && alembic upgrade head
=======
	source ./venv/bin/activate && alembic upgrade head
>>>>>>> 5b0bc22330283a4f5cbe9a6efb3e49e2e3bde92d
