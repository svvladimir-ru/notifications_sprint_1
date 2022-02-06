import time
import pika
import json

from services.notification.scheduler.email_sender import send_mail
from services.notification.config import settings


class RQBase:
    def __init__(self, routing: str = settings.RABBIT.ROUTING):
        self.host = settings.RABBIT.HOST
        self.routing = routing
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBIT.HOST))

    def open_channel(self):
        return self.connection.channel()

    def close_connection(self):
        self.connection.close()


class Consumer(RQBase):

    def callback(self, ch, method, properties, body):
        data = json.load(body)
        try:
            send_mail(to=data.get('email'),
                      subject=data.get('subject'),
                      content=data.get('content')
                      )
            time.sleep(1)
        except:
            self.open_channel().stop_consuming()
            self.start()
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start(self):
        channel = self.open_channel()
        channel.queue_declare(queue=self.routing)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(self.routing, self.callback)
        channel.start_consuming()


Consumer().start()
