from python:3.5-onbuild

EXPOSE 80

RUN apt-key adv --keyserver ha.pool.sks-keyservers.net --recv-keys B97B0AFCAA1A47F044F244A07FCC7D46ACCC4CF8

ENV PG_MAJOR 9.5
ENV PG_VERSION 9.5.0-1.pgdg80+2

RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ jessie-pgdg main' $PG_MAJOR > /etc/apt/sources.list.d/pgdg.list

RUN apt-get update \
	&& apt-get install -y postgresql-common \
	&& apt-get install -y \
		postgresql-client-$PG_MAJOR=$PG_VERSION \
		postgresql-contrib-$PG_MAJOR=$PG_VERSION \
	&& rm -rf /var/lib/apt/lists/*

CMD gunicorn --bind=0.0.0.0:80 PostgresDb.wsgi \
        --workers=1\
        --log-level=info \
        --log-file=-\
        --access-logfile=-\
        --error-logfile=-\
        --log-level=info\
        --timeout 300\
        --reload