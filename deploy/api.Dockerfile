# API: FastAPI + SQLite. Озвучка (kokoro, torch) не ставится — extra `voice` нужен только для синтеза wav.
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy PYTHONUNBUFFERED=1
WORKDIR /app/backend
COPY backend/pyproject.toml backend/uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project
COPY backend/ ./
COPY deploy/api-entrypoint.sh deploy/backup.py /app/deploy/
ENV PATH="/app/backend/.venv/bin:$PATH" SAY_DB=/data/say.db
RUN mkdir -p /data && chmod +x /app/deploy/api-entrypoint.sh
EXPOSE 8000
ENTRYPOINT ["/app/deploy/api-entrypoint.sh"]
