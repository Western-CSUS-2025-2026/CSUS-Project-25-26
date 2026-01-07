FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}
ENV APP_MODULE=api.routes.base:app
WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -U -r ./requirements.txt
COPY ./alembic.ini ./alembic.ini
COPY ./migrations ./migrations
COPY ./api ./api