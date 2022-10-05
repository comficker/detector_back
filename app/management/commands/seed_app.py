import json
from django.core.management.base import BaseCommand
from app.models import Instance, Label
from media.models import Media


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open("seed.json") as f:
            dataset = json.load(f)
            for item in dataset:
                media = Media.objects.save_url(item["external_ico"])
                instance, created = Instance.objects.get_or_create(
                    id_string=item.get("id_string"),
                    defaults={
                        "name": item["name"],
                        "callback": item["callback"],
                        "desc": item["desc"][:259],
                        "external_ico": item["external_ico"],
                        "icon": media
                    }
                )
                instance.generate_reports(False)
                if created:
                    if item.get("str_labels"):
                        for label_raw in item.get("str_labels"):
                            label, _ = Label.objects.get_or_create(
                                name=label_raw
                            )
                            instance.labels.add(label)
