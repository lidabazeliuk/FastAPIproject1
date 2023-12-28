from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import os
import dotenv

dotenv.load_dotenv(".env")
db_engine = os.environ.get("DB_ENGINE")
host = os.environ.get("DB_HOST")
user = os.environ.get("DB_USERNAME")
password = os.environ.get("DB_PASSWORD")
port = os.environ.get("DB_PORT")
database = os.environ.get("DB_DATABASE")

url = f"{db_engine}://{user}:{password}@{host}:{port}/{database}"
engine = create_engine(
    url
)

sync_session = sessionmaker(bind=engine, class_=Session, expire_on_commit=False, )


Base = declarative_base()
metadata = Base.metadata


def get_session() -> Session:
    db = sync_session()
    try:
        yield db
    finally:
        db.close()
