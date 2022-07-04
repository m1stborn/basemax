FROM python:3.8-alpine

ENV PYTHOUBUFFERED 1

WORKDIR /app

RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    && apk add libffi-dev
COPY requirements-crawler.txt .
RUN pip install --no-cache-dir -r requirements-crawler.txt

COPY . /app

#CMD [ "python", "selenium_crawler.py"]
CMD [ "python", "crawler_one.py"]