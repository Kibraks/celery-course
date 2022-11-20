#!/bin/sh

set -e

worker_ready() {
    poetry run celery -A config inspect ping
}

until worker_ready; do
  >&2 echo 'Celery workers not available'
  sleep 1
done
>&2 echo 'Celery workers are available'


exec $@