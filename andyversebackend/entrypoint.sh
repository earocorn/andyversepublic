#!/bin/sh

python manage.py migrate --no-input
python manage.py collectstatic --no-input

#command for AWS ec2 environment
#--keyfile /certs/privkey.pem --certfile /certs/fullchain.pem
gunicorn config.wsgi:application --bind 0.0.0.0:8000
#python manage.py runserver 0.0.0.0:8000