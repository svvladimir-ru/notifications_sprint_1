from scheduler.email_sender import send_mail
from abc import ABC, abstractmethod


class BaseMessage(ABC):
    @abstractmethod
    def email(self):
        pass

    @abstractmethod
    def push(self):
        pass

    @abstractmethod
    def sms(self):
        pass


class Message(BaseMessage):
    def __init__(self, message: dict):
        self.message = message

    def email(self):
        send_mail(to=self.message.get('email'),
                  subject=self.message.get('subject'),
                  content=self.message.get('content')
                  )
        return True

    def push(self):
        pass

    def sms(self):
        pass
