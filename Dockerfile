FROM python:3.10-slim

ENV POETRY_VERSION=2.1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/src/

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}" \
    && poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi

RUN poetry run python -m spacy download en_core_web_sm
RUN poetry run python -m spacy download ru_core_news_lg

ADD ./src /src
WORKDIR /src

RUN useradd --create-home appuser && chown -R appuser:appuser /src
USER appuser
