#! /usr/bin/env sh
set -e

# If there's a prestart.sh script in the /app directory, run it before starting
PRE_START_PATH=/app/prestart.sh
echo "Checking for script in $PRE_START_PATH"
if [ -f $PRE_START_PATH ] ; then
    echo "Running script $PRE_START_PATH"
    . "$PRE_START_PATH"
else
    echo "There is no script $PRE_START_PATH"
fi

# Production
python /app/src/manage.py collectstatic --noinput
python /app/src/manage.py makemigrations user --noinput
python /app/src/manage.py makemigrations --noinput
python /app/src/manage.py migrate --noinput
python /app/src/manage.py createsuperuser --noinput|| echo "superuser exists"
exec gunicorn --conf /app/gunicorn_conf.py  --bind  0.0.0.0:80 core.wsgi

