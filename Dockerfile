from python:3.5-onbuild

EXPOSE 80

RUN apt-get update \
    && apt-get install -y postgresql-client-9.4

CMD gunicorn --bind=0.0.0.0:80 PostgresDb.wsgi \
        --workers=1\
        --log-level=info \
        --log-file=-\
        --access-logfile=-\
        --error-logfile=-\
        --log-level=info\
        --timeout 30\
        --reload