FROM python:3.9

ENV PYTHONUNBUFFERED 1
EXPOSE 8000

WORKDIR /code

COPY ./requirements.txt /code/server/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/server/requirements.txt

COPY ./src /code/server/src

CMD ["uvicorn", "server.src.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]
