from fastapi import APIRouter, Depends, Body
from sqlalchemy import text
from typing import Annotated

from models.quiz import QuestionInput, AnswerInput
from routers.auth import User, get_current_user
from session import get_session

from controllers import QuizController

router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)


@router.get("/")
async def get_questions(db=Depends(get_session)):
    # return await QuizController.get_questions(db)
    return db.query(
        text("SELECT * FROM users")
    )


@router.get("/:id")
async def get_question(id: int, db=Depends(get_session)):
    return await QuizController.get_question(id, db)


@router.post("/")
async def create_question(
        question: Annotated[QuestionInput, Body(
            openapi_examples={
                "normal": {
                    "question": "Can you see the wolfs in this picture?"
                },
                "invalid": {
                    "question": 1234
                },
            },
        )],
        answers: Annotated[list[AnswerInput], Body(
            openapi_examples={
                "normal": [
                    {
                        "answer": "Yes",
                        "correct": False,
                    },
                    {
                        "answer": "No",
                        "correct": True,
                    },
                ],
                "invalid": [
                    {
                        "answer": 1234,
                        "correct": 2134,
                    },
                    {
                        "answer": 1234,
                        "correct": 1234,
                    },
                ],
            },
        )],
                          current_user: Annotated[User, Depends(get_current_user)],
                          db=Depends(get_session),
                          ):
    return await QuizController.create_question(question, answers, db)


@router.put("/answers/:id")
async def update_answer(id: int, item: AnswerInput,
                        current_user: Annotated[User, Depends(get_current_user)],
                        db=Depends(get_session)):
    return await QuizController.update_answer(id, item, db)


@router.put("/:id")
async def update_question(id: int, item: QuestionInput,
                        current_user: Annotated[User, Depends(get_current_user)],
                          db=Depends(get_session)):
    return await QuizController.update_question(id, item, db)


@router.delete("/answers/:id")
async def delete_answer(id: int,
                        current_user: Annotated[User, Depends(get_current_user)],
                        db=Depends(get_session)):
    return await QuizController.delete_answer(id, db)


@router.delete("/:id")
async def delete_question(id: int,
                        current_user: Annotated[User, Depends(get_current_user)],
                          db=Depends(get_session)):
    return await QuizController.delete_question(id, db)
