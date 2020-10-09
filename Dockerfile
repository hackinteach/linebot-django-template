FROM python:3.7
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN apt-get update && apt-get install -y python-pygraphviz postgresql-client && rm -rf /var/lib/apt/lists/*
#RUN pip install pipenv
ADD requirements.txt .
#ADD Pipfile.lock .
#RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt
ADD . .

# uWSGI will listen on this port
EXPOSE 8000

# Call collectstatic (customize the following line with the minimal environment variables needed for manage.py to run):
#RUN python manage.py collectstatic --noinput

# Tell uWSGI where to find your wsgi file (change this):
ENV UWSGI_WSGI_FILE=LineBotBackend/wsgi.py

# Base uWSGI configuration (you shouldn't need to change these):
ENV UWSGI_MASTER=1 UWSGI_HTTP_AUTO_CHUNKED=1 UWSGI_HTTP_KEEPALIVE=1 UWSGI_LAZY_APPS=1 UWSGI_WSGI_ENV_BEHAVIOR=holy

# Number of uWSGI workers and threads per worker (customize as needed):
ENV UWSGI_WORKERS=1 UWSGI_THREADS=4

# uWSGI static file serving configuration (customize or comment out if not needed):
#ENV UWSGI_STATIC_MAP="/backend/static/=/code/backend/static/" UWSGI_STATIC_EXPIRES_URI="/backend/static/.*\.[a-f0-9]{12,}\.(css|js|png|jpg|jpeg|gif|ico|woff|ttf|otf|svg|scss|map|txt) 315360000"
ENV DJANGO_MANAGEPY_MIGRATE="xon"
# Deny invalid hosts before they get to Django (uncomment and change to your hostname(s)):
# ENV UWSGI_ROUTE_HOST="^(?!localhost:8000$) break:400"

ENV GAE_APPLICATION=TRUE

# Uncomment after creating your docker-entrypoint.sh
# ENTRYPOINT ["/code/docker-entrypoint.sh"]

RUN chmod +x /app/docker-entrypoint.sh

# Start uWSGI
ENTRYPOINT ["/app/docker-entrypoint.sh"]

#CMD ["uwsgi", "--http", ":$PORT"]
CMD gunicorn LineBotBackend.wsgi:application -b :$PORT --timeout 0