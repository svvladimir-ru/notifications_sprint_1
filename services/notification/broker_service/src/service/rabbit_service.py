import pika
import backoff
import requests
from fastapi import Depends
from sqlalchemy.orm.session import Session

from core import settings
from database.rabbit import get_rabbit
from database.database import Others, Welcome, Template, User
from database.db import get_db


class RQBase:
    def __init__(self,
                 connection: pika.BlockingConnection(
                     pika.ConnectionParameters(settings.RABBIT.HOST)) = Depends(get_rabbit),
                 routing: str = settings.RABBIT.ROUTING):
        self.routing = routing
        self.connection = connection

    def open_channel(self):
        return self.connection().channel()

    def close_connection(self):
        self.connection().close()


class RQWorker(RQBase):
    def __init__(self, pk: str):
        super().__init__()
        self.id = pk

    @backoff.on_exception(backoff.expo, Exception, max_tries=10)
    def on_massage(self):
        data = getattr(self, self.routing.lower())
        self.open_channel().basic_publish(exchange=settings.RABBIT.EXCHANGE,
                                          routing_key=self.routing,
                                          body=data)
        return True

    @backoff.on_exception(backoff.expo, Exception, max_tries=10)
    def welcome(self, db: Session = Depends(get_db)):
        welcome = db.query(Welcome).get(id)
        template = db.query(Template).get(welcome.template_id)
        user = db.query(User).get(welcome.user_id)
        return {
            'email': user.email,
            'content': {
                'username': user.username,
                'template': template.template,
                'link': self.bitly(f'http://localhost/{self.routing.lower()}/')
            },
            'subject': template.name,
        }

    @backoff.on_exception(backoff.expo, Exception, max_tries=10)
    def other(self, db: Session = Depends(get_db)):
        users = db.query(User).all()
        massage = db.query(Others).get(id)
        list_user = list(i.email for i in users.email)

        return {
            'email': list_user,
            'content': {
                'template': db.query(Template).get(massage.template_id).template,
                'description': massage.description,
                'unsubscribe': self.bitly(f'http://localhost/{self.routing.lower()}/')
            },
            'subject': massage.title,
        }

    def bitly(self, uri):
        query_params = {
            "long_url": uri
        }
        header = {'Content-Type': 'application/json',
                  'Authorization': f'Bearer {settings.BITLY_ACCESS_TOKEN}'
                  }

        endpoint = 'https://app.bitly.com/v4/shorten'
        try:
            response = requests.post(endpoint, headers=header, data=query_params, verify=False)
            return response.json()
        except:
            return 'http://localhost:8000'
