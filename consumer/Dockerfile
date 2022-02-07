# pull official base image
FROM python:3.9.7-slim
# set work directory
WORKDIR /usr/src/consumer
# set environment variables
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
# install dependencies
COPY requirements.txt .
RUN apt-get clean && apt-get update && apt-get install -y build-essential netcat
RUN pip install --no-cache-dir --upgrade -r requirements.txt
# copy project
COPY . .
ENTRYPOINT ["sh", "/usr/src/consumer/entrypoint.sh"]