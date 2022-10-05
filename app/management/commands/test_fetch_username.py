from django.core.management.base import BaseCommand
from utils.helpers import get_username
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        usernames = get_username(1)
        for un in usernames:
            User.objects.create_user(
                username=un,
                email="{username}@gmail.com".format(username=un),
                password="XXXXXXXXXXXXXXXXXXXXXY"
            )
