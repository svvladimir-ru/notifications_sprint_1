# pull official base image
FROM python:3.9-alpine
# set work directory
WORKDIR /usr/src/events_etl
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# install postgresql dependencies
RUN apk update --no-cache \
    && apk add gcc musl-dev python3-dev libffi-dev openssl-dev cargo postgresql-dev
# install dependencies
RUN pip install --upgrade pip
RUN pip install poetry
COPY ./pyproject.toml .
RUN poetry config virtualenvs.create false
RUN poetry install
# copy project
COPY . .
ENTRYPOINT ["sh", "/usr/src/events_etl/entrypoint.sh"]