FROM python:latest
MAINTAINER Matt Rasband <matt.rasband@gmail.com>
RUN mkdir -p /app
WORKDIR /app
ADD requirements.txt .
RUN pip install -Ur requirements.txt
ADD . .
EXPOSE 8080
CMD gunicorn drudge.application:app --bind 0.0.0.0:8080 --worker-class aiohttp.worker.GunicornWebWorker
