#!/bin/sh

python manage.py migrate
python scripts/create_user_and_token.py
exec "$@"
