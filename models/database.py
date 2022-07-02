from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import Setting

config = Setting()

engine = create_engine(config.DATABASE_URL.replace("postgres://", "postgresql://", 1))
Base = declarative_base()


def create_session():
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_local()

    return session


def create_table():
    Base.metadata.create_all(engine)


def drop_table():
    Base.metadata.drop_all(engine)

