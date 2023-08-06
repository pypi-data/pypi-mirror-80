from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = 'Displays current date & time'

    def handle(self, *args, **kwargs):
        time = timezone.localtime().strftime("%A - %d/%m/%Y, %H:%M:%S %p")
        self.stdout.write(self.style.SUCCESS("Today is {}".format(time)))
