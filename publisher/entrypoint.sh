#!/bin/sh
echo "PostgreSQL not yet run..."
# Проверяем доступность хоста и порта
while ! nc -z $NOTIFIC_POSTGRES_HOST $NOTIFIC_POSTGRES_PORT; do
  sleep 0.1
done
echo "PostgreSQL did run."

# если база еще не запущена
echo "RabbitMQ not yet run..."
# Проверяем доступность хоста и порта
while ! nc -z $NOTIFIC_RABBIT_HOST $NOTIFIC_RABBIT_PORT; do
  sleep 0.1
done
echo "RabbitMQ did run."

gunicorn main:app --bind 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker