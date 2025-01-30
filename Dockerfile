FROM python:3.11-alpine

RUN apk update &&  \
    apk upgrade &&  \
    apk add --no-cache build-base libffi-dev bash

WORKDIR /src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./ /src