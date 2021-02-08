FROM python:3.7-alpine
MAINTAINER Riaan Swart

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
# RUN apk add --update --no-cache --virtual .tmp-build-deps \
#         gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev
RUN pip install -r /requirements.txt
# RUN apk del .tmp-build-deps

RUN mkdir /recipes
WORKDIR /recipes
COPY ./recipes /recipes

RUN adduser -D user
USER user
