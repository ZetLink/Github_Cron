FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y python3 python3-pip git cron git && \
    apt-get clean

WORKDIR /app

COPY script.py /app/script.py
COPY crontab.txt /etc/cron.d/github-cron

RUN pip3 install requests

RUN chmod 0644 /etc/cron.d/github-cron

RUN crontab /etc/cron.d/github-cron

CMD ["cron", "-f"]
