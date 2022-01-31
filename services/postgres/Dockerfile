# pull official base image
FROM postgres:13.0-alpine
# set listening port
EXPOSE 5432/tcp
# set work directory
WORKDIR /var/lib/postgresql/data/
# copy db schema and create all table
COPY ./db_events.sql /docker-entrypoint-initdb.d/
COPY ./db_users.sql /docker-entrypoint-initdb.d/

