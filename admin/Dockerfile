# pull official base image
FROM python:3.9-alpine
# set listening port
EXPOSE 8000/tcp
# set work directory
WORKDIR /usr/src/admin
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install postgresql dependencies
RUN apk update --no-cache \
    && apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo postgresql-dev
# install dependencies
RUN pip install --upgrade pip poetry
COPY ./pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install
# copy project
COPY . .