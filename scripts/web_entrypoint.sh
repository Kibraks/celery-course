#!/bin/sh

set -e

poetry run python manage.py wait_for_db
poetry run python manage.py migrate

exec $@
