FROM python:3.13

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction

COPY . .

CMD ["celery", "-A", "service.email_service", "worker", "--loglevel=info"]

