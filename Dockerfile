FROM python:3.8-alpine

ENV PYTHOUBUFFERED 1

WORKDIR /app

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev
COPY crawler_requirements.txt .
RUN pip install --no-cache-dir -r crawler_requirements.txt

COPY . /app

CMD [ "python", "selenium_crawler.py", "--local" ]