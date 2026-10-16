from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.accounts.progress import router as progress_router
from app.accounts.router import router as auth_router
from app.accounts.schema import init_accounts
from app.accounts.service import ensure_default_users
from app.books.router import router as books_router
from app.books.service import db, init_db
from app.exercises.router import router as exercises_router
from app.exercises.store import ensure_tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    with db() as conn:
        init_db(conn)
        init_accounts(conn)
        ensure_tasks(conn)
        ensure_default_users(conn)
    yield


app = FastAPI(title="Say — Russian TTS course app", lifespan=lifespan)

app.include_router(auth_router)
app.include_router(progress_router)
app.include_router(books_router)
app.include_router(exercises_router)
