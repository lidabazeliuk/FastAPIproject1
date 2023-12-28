from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from session import Base
from pydantic import BaseModel


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    question = Column(String(128))

    answers = relationship("Answer", back_populates="questions")

    def __repr__(self):
        return f"{self.__dict__}"


class QuestionInput(BaseModel):
    question: str


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))

    answer = Column(String(128))
    correct = Column(Boolean, default=False)

    questions = relationship("Question", back_populates="answers")

    def __repr__(self):
        return f"{self.__dict__}"


class AnswerInput(BaseModel):
    answer: str
    correct: bool
