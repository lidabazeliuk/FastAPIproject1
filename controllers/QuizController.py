from fastapi import Depends, Response, HTTPException, status
from sqlalchemy.orm import joinedload

from models.quiz import Question, Answer
from session import get_session


class QuizController:
    @staticmethod
    async def get_questions(db):
        questions = (
            db.query(Question)
            .join(Question.answers)
            .options(
                joinedload(Question.answers)
            )
            .all()
        )
        return {"response": questions}

    @staticmethod
    async def get_question(id: int, db=Depends(get_session)):
        question = (
            db.query(Question)
            .join(Question.answers)
            .filter(Question.id == id)
            .options(
                joinedload(Question.answers)
            )
            .first()
        )
        return {"response": question}

    @staticmethod
    async def create_question(question, answers, db):
        question = Question(**question.dict())
        db.add(question)
        db.commit()

        for answer in answers:
            answer = Answer(**answer.dict(), question_id=question.id)
            db.add(answer)

        else:
            db.commit()

        return Response("Successfully created", 201)

    @staticmethod
    async def update_answer(id, item, db):
        answer = db.query(Answer).filter(Answer.id == id)

        if answer.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer with such id not found")
        else:
            answer.update(item.dict())
            db.commit()

        return Response("Successfully updated", 200)

    @staticmethod
    async def update_question(id, item, db):
        question = db.query(Question).filter(Question.id == id)

        if question.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question with such id not found")
        else:
            question.update(item.dict())
            db.commit()

        return Response("Successfully updated", 200)

    @staticmethod
    async def delete_answer(id, db):
        answer = db.query(Answer).get(id)

        if answer is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Answer with such id not found")
        else:
            db.delete(answer)
            db.commit()

        return Response("Successfully deleted", 200)

    @classmethod
    async def delete_question(cls, id, db):
        question = db.query(Question).get(id)

        if question is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question with such id not found")
        else:
            db.delete(question)

            answers = db.query(Answer).filter(Answer.question_id == id).all()

            for answer in answers:
                await cls.delete_answer(answer.id, db)
            else:
                db.commit()

        return Response("Successfully deleted", 200)