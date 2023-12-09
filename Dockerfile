FROM python:3.11

EXPOSE 8000

WORKDIR /app

ENV POETRY_VERSION=1.5.0 \
    POETRY_HOME="/opt/poetry" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_VIRTUALENVS_CREATE=true \
    PATH="$POETRY_HOME/bin:/app/.venv/bin:$PATH"

RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s $POETRY_HOME/bin/poetry /usr/local/bin/poetry

COPY pyproject.toml poetry.lock /app/

COPY ./src /app/src
COPY ./README.md /app/README.md

RUN poetry install --no-dev


CMD ["uvicorn", "src.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
