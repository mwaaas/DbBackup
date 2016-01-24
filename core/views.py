from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import render
from .backup_restore_db import backup
from .dropbox.upload_download import upload
from structlog import  get_logger
from django.conf import settings
import os

class Home(View):

    def get(self, req):
        return render(req, template_name='home.html')

    def post(self, req):
        self.logger = get_logger(__name__).bind(action='backup_request')

        self.logger.info('starting')
        file_path = backup()
        self.logger.info('backup_file', path=file_path)

        self.logger.info('starting_upload')
        upload_response = self.upload_file(file_path)
        self.logger.info('done_uploading', response=str(upload_response))
        return self.get(req)

    def upload_file(self, file_path):
        # At the moment only dropbox is supported
        backup_cloud_list = settings.BACKUP_CLOUD_LIST

        if backup_cloud_list.get('dropbox'):
            upload(file_path)
            os.remove(file_path) if os.path.exists(file_path) else None
        else:
            self.logger.warn("only dropbox is supported at the moment")

