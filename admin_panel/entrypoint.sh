#!/bin/sh


#python manage.py makemigrations

python manage.py migrate auth
python manage.py migrate contenttypes
python manage.py migrate admin
python manage.py migrate sessions
python manage.py makemigrations django_summernote
python manage.py migrate django_summernote
python manage.py migrate administrator

python manage.py migrate authentication --database auth_db
python manage.py migrate movie --database movie_db
python manage.py migrate notification --database notification_db

python manage.py makemigrations user_profile
python manage.py migrate user_profile --database profile_db

python manage.py collectstatic --noinput

gunicorn --bind 0.0.0.0:8000 config.wsgi:application

exec "$@"