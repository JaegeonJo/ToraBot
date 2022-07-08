FROM python:3.8.13-slim-bullseye

RUN apt-get update && apt-get install -y libffi-dev libnacl-dev python3-dev

COPY requirements.txt .
RUN pip install -r requirements.txt

WORKDIR /app