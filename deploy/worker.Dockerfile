# Code-check worker: the Python standard library + docker CLI. It needs no database; sandboxes run in dind.
FROM python:3.14-slim
COPY --from=docker:29-cli /usr/local/bin/docker /usr/local/bin/docker
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY worker/worker.py worker/runner.py ./
# build context of cs-core-rust-crates:1 and the image loading script (service `images`)
COPY worker/docker /app/docker
COPY deploy/init-images.sh /app/init-images.sh
RUN chmod +x /app/init-images.sh
CMD ["python", "worker.py"]
