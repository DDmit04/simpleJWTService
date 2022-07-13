FROM python:3.9-alpine


COPY ./docker/cron/cron_jobs /app/mycron
RUN mkdir "/logs"
RUN touch /logs/output.log
RUN touch /logs/err.log
RUN crontab /app/mycron

WORKDIR /app
COPY . /app
RUN pip install -r ./src/requirements.txt