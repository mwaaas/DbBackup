from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import render
from structlog import  get_logger
from django.conf import settings
from .backup_restore_db import restore_db
from django.core import management
import copy
from dbbackup.storage.base import BaseStorage


class Home(View):

    def get(self, req):
        logger = get_logger(__name__)
        logger.info('request_data', data=req.GET)
        backup_list = self.list_backups()
        if req.GET.get('path'):
            self.restore_db(req.GET['path'])

        return render(req, 'home.html',
                      {'backup_list': backup_list})

    def post(self, req):
        self.backup_db()
        return self.get(req)

    @staticmethod
    def backup_db():
        previouse_db_configuration = copy.deepcopy(settings.DATABASES)
        # hack hack !!!!!
        # its not recommended to alter django settings at runtime
        # doing this for django-db backup to work even if Database settings has not been defined
        settings.DATABASES = settings.DBBACKUP_DATABASES
        management.call_command('dbbackup')
        settings.DATABASES = previouse_db_configuration

    @staticmethod
    def list_backups():
        storage = BaseStorage.storage_factory()
        return storage.list_backups()


    @staticmethod
    def restore_db(file_name):
        previouse_db_configuration = copy.deepcopy(settings.DATABASES)
        # hack hack !!!!!
        # its not recommended to alter django settings at runtime
        # doing this for django-db backup to work even if Database settings has not been defined
        settings.DATABASES = settings.DBBACKUP_DATABASES
        #management.call_command('dbrestore -f {0}'.format(file_name))
        management.call_command('dbrestore', interactive=False,
                                filepath=file_name)
        settings.DATABASES = previouse_db_configuration
