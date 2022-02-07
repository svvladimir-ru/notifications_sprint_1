from pydantic import BaseSettings, AnyUrl


class RabbitMQSettings(BaseSettings):
    USERNAME: str = 'rabbit'
    PASSWORD: str = 'rabbit'
    HOST: str = 'rabbitmq'
    PORT: int = 5672
    DSN: AnyUrl = f"amqp://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/%2F"
    EXCHANGE: str = ''
    ROUTING: str = 'welcome'

    class Config:
        env_prefix = "RABBIT_"


class Base(BaseSettings):
    SMTP_HOST: str = 'smtp.gmail.com'
    SMTP_PORT: int = 465
    SMTP_USER: str
    SMTP_PASSWORD: str
    RABBIT: RabbitMQSettings = RabbitMQSettings()

    class Config:
        env_file = '.env'


settings = Base()
