from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.books.router import router as books_router
from app.books.service import db, init_db
from app.exercises.router import router as exercises_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    with db() as conn:
        init_db(conn)
    yield


app = FastAPI(title="Say — Russian TTS course app", lifespan=lifespan)

app.include_router(books_router)
app.include_router(exercises_router)
