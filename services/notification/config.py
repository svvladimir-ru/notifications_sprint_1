from pydantic import BaseSettings, AnyUrl, validator, RedisDsn, PostgresDsn


class RabbitMQSettings(BaseSettings):
    USERNAME: str = 'rabbit'
    PASSWORD: str = 'rabbit'
    HOST: str = 'rabbitmq'
    PORT: int = 5672
    DSN: AnyUrl = 'amqp://rabbit:rabbit@127.0.0.1:5672/%2F'
    EXCHANGE: str = ''
    ROUTING: str = 'welcome'

    class Config:
        env_prefix = "RABBIT_"


class PostgresSettings(BaseSettings):
    USERNAME: str = 'postgres'
    PASSWORD: str = 'postgres'
    HOST: str = 'postgres_notification'
    PORT: int = 5432
    DB: str = 'events'
    POSTGRES_DSN: AnyUrl = f'postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}'

    class Config:
        env_file = '.env'
        env_prefix = "NOTIFIC_POSTGRES"


class Base(BaseSettings):
    SMTP_HOST: str = 'smtp.gmail.com'
    SMTP_PORT: int = 465
    SMTP_USER: str
    SMTP_PASSWORD: str
    POSTGRES: PostgresSettings = PostgresSettings()
    RABBIT: RabbitMQSettings = RabbitMQSettings()

    class Config:
        env_file = '.env'


settings = Base()
