from pathlib import Path

from pydantic import BaseSettings, AnyUrl, validator, RedisDsn, PostgresDsn


class RabbitMQSettings(BaseSettings):
    USERNAME: str = 'rabbit'
    PASSWORD: str = 'rabbit'
    HOST: str = 'rabbitmq'
    PORT: int = 5672
    DSN: AnyUrl = 'amqp://rabbit:rabbit@rabbitmq:5672/%2F'
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
        env_prefix = "NOTIFIC_POSTGRES"


class Base(BaseSettings):
    PROJECT_NAME: str = 'RabbitService'
    SENTRY_DSN: str = 'NOTIFIC_SENTRY_DSN'
    POSTGRES: PostgresSettings = PostgresSettings()
    RABBIT: RabbitMQSettings = RabbitMQSettings()
    BITLY_ACCESS_TOKEN: str
