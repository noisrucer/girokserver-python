FROM python:3.11

EXPOSE 8000

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY ./girok ./girok

CMD ["python", "-m", "girok", "--host", "0.0.0.0", "--port", "8080"]
