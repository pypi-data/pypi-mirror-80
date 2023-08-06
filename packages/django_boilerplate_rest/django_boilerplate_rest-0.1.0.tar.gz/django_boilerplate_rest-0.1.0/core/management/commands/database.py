from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError
from django.conf import settings


class Command(BaseCommand):
    help = "Check the existing database connection"

    def print_notice(self, message):
        return self.stdout.write(self.style.NOTICE(message))

    def handle(self, *args, **options):
        default_db = settings.DATABASES['default']
        self.print_notice('Connecting database...')
        self.print_notice("DSN for database 'default' with engine '{}'".format(default_db['ENGINE']))
        self.print_notice("host='{}' port='{}' dbname='{}' username='{}' password='{}' ".format(
            default_db['HOST'],
            default_db['PORT'],
            default_db['NAME'],
            default_db['USER'],
            default_db['PASSWORD']
        ))
        try:
            connection.ensure_connection()
            self.stdout.write(self.style.SUCCESS('Database connection available!!!'))
        except OperationalError as error:
            self.stdout.write(self.style.ERROR('Database configuration failed!!!, {}'.format(error)))
