#!/bin/bash
docker build -t github-cron .
docker run -d --name github-cron-container -v /{REPOSITORY_PATH}:/app/{PATH_IN_CONTAINER} github-cron
