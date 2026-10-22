# Сборка фронтенда и Caddy: HTTPS, статика, /api → api. /internal (API воркеров) наружу не отдаётся.
FROM node:22 AS web
WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM caddy:2
COPY --from=web /app/frontend/dist /srv
COPY deploy/Caddyfile /etc/caddy/Caddyfile
