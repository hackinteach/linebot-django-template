#!/bin/sh
set -e

#DATABASE_URL="postgres://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"
#
#until psql $DATABASE_URL -c '\l'; do
#    >&2 echo "Postgres is unavailable - sleeping"
#    sleep 1
#done
#
#>&2 echo "Postgres is up - continuing"

if [ "$DJANGO_MANAGEPY_MIGRATE" = 'xon' ]; then
    python manage.py migrate --noinput
    python manage.py loaddata LineBotBackend/fixtures/user.json
    # remove line below on production
    python manage.py collectstatic --noinput
fi

exec "$@"