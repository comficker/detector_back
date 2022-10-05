import json
from django.core.management.base import BaseCommand
from app.models import Instance, Label


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open("seed.json") as f:
            dataset = json.load(f)
            for item in dataset:
                instance, created = Instance.objects.get_or_create(
                    id_string=item.get("id_string"),
                    defaults=item
                )
                instance.generate_reports(False)
                if created:
                    if item.get("labels"):
                        for label_raw in item.get("labels"):
                            label, _ = Label.objects.get_or_create(
                                name=label_raw
                            )
                            instance.labels.add(label)
