#!/bin/sh
# если база еще не запущена
echo "RabbitMQ not yet run..."

# Проверяем доступность хоста и порта
while ! nc -z $RABBIT_HOST $RABBIT_PORT; do
  sleep 0.1
done

echo "RabbitMQ did run."

python email_consumer.py