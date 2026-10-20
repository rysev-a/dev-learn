"""Внутренний API для воркеров проверки: забрать задание, подтвердить жизнь, вернуть результат.
Закрыт токеном SAY_WORKER_TOKEN (заголовок Authorization: Bearer …); без токена в окружении недоступен вовсе."""

import asyncio
import secrets
import time

from anyio import to_thread
from fastapi import APIRouter, Header, HTTPException, Response
from pydantic import BaseModel, Field

from app import config
from app.books.service import db
from app.exercises import jobs

router = APIRouter(prefix="/internal/worker", tags=["worker"])

MAX_WAIT = 25


def _auth(authorization: str | None) -> None:
    token = config.WORKER_TOKEN
    if not token:
        raise HTTPException(404, "Not found")
    given = (authorization or "").removeprefix("Bearer ").strip()
    if not secrets.compare_digest(given.encode(), token.encode()):
        raise HTTPException(401, "Неверный токен воркера")


class ClaimIn(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    lanes: list[str] = Field(max_length=4)
    slots: int = Field(default=1, ge=1, le=256)
    wait: int = Field(default=20, ge=0, le=MAX_WAIT)


class PingIn(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    lanes: list[str] = Field(max_length=4)
    slots: int = Field(default=1, ge=1, le=256)
    jobs: list[str] = Field(default_factory=list, max_length=100)


class ResultIn(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    result: dict


def _claim(name: str, lanes: list[str], slots: int) -> dict | None:
    with db() as conn:
        jobs.ping(conn, name, lanes, slots, [])
        return jobs.claim(conn, name, lanes)


@router.post("/claim")
async def claim(body: ClaimIn, authorization: str | None = Header(default=None)):
    """Долгий опрос: до `wait` секунд ждёт задание из полос воркера; пусто — 204."""
    _auth(authorization)
    deadline = time.monotonic() + body.wait
    while True:
        job = await to_thread.run_sync(_claim, body.name, body.lanes, body.slots)
        if job is not None:
            return job
        if time.monotonic() >= deadline:
            return Response(status_code=204)
        await asyncio.sleep(0.4)


@router.post("/ping", status_code=204)
def ping(body: PingIn, authorization: str | None = Header(default=None)):
    _auth(authorization)
    with db() as conn:
        jobs.ping(conn, body.name, body.lanes, body.slots, body.jobs)


@router.post("/jobs/{job_id}/result", status_code=204)
def result(job_id: str, body: ResultIn, authorization: str | None = Header(default=None)):
    _auth(authorization)
    with db() as conn:
        if not jobs.complete(conn, job_id, body.name, body.result):
            raise HTTPException(409, "Задание уже не за этим воркером (аренда истекла или результат принят)")
