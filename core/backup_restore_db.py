import os
import uuid
from django.conf import settings
from structlog import get_logger


def backup():
    logger = get_logger(__name__).bind(
        action='backup_db'
    )
    logger.info('starting')
    command = 'pg_dump -U ' \
              '{username} -h {host} -p {port} -F tar -O -d {db_name} -f {file} -w'
    if settings.POSTGRES_PASSWORD:
        command = 'PGPASSWORD={password} ' + command

    file_path = '/usr/src/app/core/dump_file_{unique_id}.tar'.format(unique_id=uuid.uuid4())

    full_command = command.format(password=settings.POSTGRES_PASSWORD,
                                  username=settings.POSTGRES_USER,
                                  host=settings.POSTGRES_HOST,
                                  port=settings.POSTGRES_PORT,
                                  file=file_path,
                                  db_name=settings.POSTGRES_DB
                                  )

    logger.debug('full_command', command=full_command)
    os.system(full_command)

    logger.debug('finished_successfully')

    return file_path


def restore_db(file_name):
    logger = get_logger(__name__).bind(
        action='restore_db'
    )
    logger.info('starting')
    command = "pg_restore --verbose --clean --no-acl --no-owner" \
              " -h {host}  -p {port}  -U {username} -d {db_name} {file_path}"

    if settings.POSTGRES_PASSWORD:
        command = 'PGPASSWORD={password} ' + command

    file_path = "/usr/src/app/core/{}".format(file_name)

    full_command = command.format(
        password=settings.POSTGRES_PASSWORD,
        username=settings.POSTGRES_USER,
        host=settings.POSTGRES_HOST,
        port=settings.POSTGRES_PORT,
        file_path=file_path,
        db_name=settings.POSTGRES_DB
    )
    logger.debug('full_command', command=full_command)

    os.system(full_command)

    logger.debug('finished successfully')


#'PGPASSWORD=mysecretpassword pg_dump -U postgres -h db -p 5432 -d slash_air -w'
# pg_dump -h db -p 5432 -F c -O -U postgres postgres > backup.dump
# pg_restore --verbose --clean --no-acl --no-owner -h db  -p 5432  -U postgres -d postgres backup.dump
# /usr/src/app/core