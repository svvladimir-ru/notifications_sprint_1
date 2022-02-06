FROM python:3.9.7-buster
WORKDIR /sites
COPY broker_service/src/requirements/base.txt /sites
RUN pip install -r /sites/base.txt --no-cache-dir
COPY ./scheduler /sites/scheduler
COPY email_consumer.py /sites
COPY config.py /sites

EXPOSE 8000
CMD ["python", "email_consumer.py"]