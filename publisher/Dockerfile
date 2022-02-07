# pull official base image
FROM python:3.9.7-slim
# set work directory
WORKDIR /usr/src/publisher
# set environment variables
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
# install dependencies
COPY requirements/base.txt .
RUN apt-get clean && apt-get update && apt-get install -y build-essential netcat
RUN pip install --no-cache-dir --upgrade -r base.txt
# copy project
COPY . .
ENTRYPOINT ["sh", "/usr/src/publisher/entrypoint.sh"]