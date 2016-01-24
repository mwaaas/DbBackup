__author__ = 'Mwaaas'
__email__ = 'francismwangi152@gmail.com'
__phone_number__ = '+254702729654'

import dropbox
from django.conf import settings
from dropbox.exceptions import ApiError, AuthError
import sys
from dropbox.files import WriteMode
from structlog import get_logger


def get_client(auth_token):
    client = dropbox.Dropbox(auth_token)
    logger = get_logger(__name__)
    logger.info('linked_account', client=str(client))
    # Check that the access token is valid
    try:
        client.users_get_current_account()
    except AuthError as err:
        sys.exit("ERROR: Invalid access token; try re-generating an access token from the app console on the web.")

    return client


def upload(file_path):
    logger = get_logger(__name__).bind(action='upload', storage='dropbox')

    # dropbox configuration
    dropbox_confs = settings.BACKUP_CLOUD_LIST['dropbox']
    backup_abs_path = dropbox_confs['path']
    auth_token = dropbox_confs["DROP_BOX_AUTH_TOKEN"]

    logger.info('file_uploading', path=file_path)
    backup_path = file_path.split('/')[-1]
    with open(file_path, 'r') as f:
        backup_path = "{0}{1}".format(backup_abs_path, backup_path)
        logger.info('start_uploading', backup_path=backup_path)
        try:
            dbx = get_client(auth_token)
            dbx.files_upload(f, backup_path, mode=WriteMode('overwrite'))
            logger.info('finished_uploading')
        except ApiError as err:
            # This checks for the specific error where a user doesn't have
            # enough Dropbox space quota to upload this file
            if (err.error.is_path() and
                    err.error.get_path().error.is_insufficient_space()):
                sys.exit("ERROR: Cannot back up; insufficient space.")
            elif err.user_message_text:
                logger.info(err.user_message_text)
                sys.exit()
            else:
                logger.info(err)
                sys.exit()

    logger.info('Uploaded_successfully')


# Restore the local and Dropbox files to a certain revision
def restore(file):
    dbx = get_client()

    # Download the specific revision of the file at BACKUPPATH to LOCALFILE
    print("Downloading current " + file + " from Dropbox")
    resp = dbx.files_download(file)

    resp
