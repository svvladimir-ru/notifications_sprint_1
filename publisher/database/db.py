from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from core import settings


engine = create_engine(settings.POSTGRES.POSTGRES_DSN)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

db = SessionLocal()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
