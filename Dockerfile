FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc curl && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN curl -sSL https://install.python-poetry.org | python3

ENV PATH="/root/.local/bin:$PATH"
ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml poetry.lock README.md ./

RUN poetry install --no-interaction --no-ansi --no-root

COPY mysite .
COPY diploma-frontend/dist/ .
RUN mkdir "static"

RUN pip install diploma-frontend-0.6.tar.gz

EXPOSE 8000
