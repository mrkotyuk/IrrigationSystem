FROM python:3.12.7-slim-bullseye

RUN apt update -y && \
    apt install -y python3-dev gcc musl-dev libpq-dev nmap

ENV PYTHONUNBUFFERED=1
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . /app
