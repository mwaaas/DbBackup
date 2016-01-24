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
              '{username} -h {host} -p {port} -d {db_name} -f {file} -w'
    if settings.POSTGRES_PASSWORD:
        command = 'PGPASSWORD={password} ' + command

    file_path = '/usr/src/app/core/dump_file_{unique_id}.backup'.format(unique_id=uuid.uuid4())

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


#'PGPASSWORD=mysecretpassword pg_dump -U postgres -h db -p 5432 -d slash_air -w'