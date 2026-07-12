FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml README.md ./
COPY src ./src
COPY config ./config

RUN uv pip install --system --no-cache .

ENTRYPOINT ["atlas"]
CMD ["doctor"]
