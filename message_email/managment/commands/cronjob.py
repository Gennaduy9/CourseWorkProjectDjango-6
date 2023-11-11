from django.core.management import BaseCommand

from ...services import cronjob


class Command(BaseCommand):
    def handle(self, *args, **options):
        cronjob()
