from sqlalchemy import Column, Integer, String
from session import Base
from pydantic import BaseModel


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    nickname = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)


class UserBody(BaseModel):
    username: str
    nickname: str
    email: str


class UserCreating(UserBody):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
