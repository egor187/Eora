import db
from bot import Bot
from fa_dependencies import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends

app = FastAPI()

db.Base.metadata.create_all(bind=db.engine)


@app.get("/start/{user_id}")
async def root(user_id: str, db: Session = Depends(get_db)):
    bot = Bot(user_id, db)
    return bot.start_dialogue()


@app.post("/answer/{user_id}/{answer}")
async def process_answer(user_id: str, answer: str):
    bot = Bot(user_id)
    bot.process_answer(answer=answer)
    return {"message": f"Processing answer"}
