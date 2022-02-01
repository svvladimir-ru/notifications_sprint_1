#!/bin/sh

if [ $1 = "migrate" ]
then
  if [ "$DATABASE" = "postgres" ]
  then
      # если база еще не запущена
      echo "DB not yet run..."

      # Проверяем доступность хоста и порта
      while ! nc -z $DB_HOST $DB_PORT; do
        sleep 0.1
      done

      echo "DB did run."
  fi
  # Выполняем миграции
  python manage.py migrate
  python manage.py createsuperuser \
        --noinput \
        --username $DJANGO_SUPERUSER_USERNAME \
        --email $DJANGO_SUPERUSER_EMAIL
else
  python manage.py collectstatic --noinput
fi

gunicorn -c './gunicorn_conf.py' config.wsgi
exec "$@"