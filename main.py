from fastapi import FastAPI
from routers import quiz, auth

app = FastAPI(
    title="Quiz",
    version="1.0.0",
)
app.include_router(quiz.router)
app.include_router(auth.router)


@app.get("/")
async def home():
    return {"response": 200}
