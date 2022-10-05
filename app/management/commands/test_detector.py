from django.core.management.base import BaseCommand
from utils.detector import check_status


class Command(BaseCommand):
    def handle(self, *args, **options):
        print(check_status("https://google.com"))
