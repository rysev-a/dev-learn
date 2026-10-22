# Воркер проверки кода: стандартная библиотека Python + docker CLI. База ему не нужна, песочницы запускаются в dind.
FROM python:3.14-slim
COPY --from=docker:29-cli /usr/local/bin/docker /usr/local/bin/docker
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY backend/worker.py ./
COPY backend/app/__init__.py ./app/
COPY backend/app/exercises/__init__.py backend/app/exercises/runner.py ./app/exercises/
# контекст сборки say-rust-crates:1 и скрипт заливки образов (сервис `images`)
COPY backend/docker /app/docker
COPY deploy/init-images.sh /app/init-images.sh
RUN chmod +x /app/init-images.sh
CMD ["python", "worker.py"]
