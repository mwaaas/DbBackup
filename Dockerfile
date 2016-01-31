from python:3.5-onbuild

EXPOSE 80

RUN apt-get update \
    && apt-get install -y apt-utils\
    && apt-get install -y postgresql-client-9.4
#RUN python manage.py migrate
CMD gunicorn --bind=0.0.0.0:80 PostgresDb.wsgi \
        --workers=1\
        --log-level=info \
        --log-file=-\
        --access-logfile=-\
        --error-logfile=-\
        --log-level=info\
        --timeout 300\
        --reload