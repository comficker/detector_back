import random
import json
from django.db import models
from base.interface import BaseModel, HasIDString
from django.contrib.auth.models import User
from media.models import Media
from django.utils import timezone


# Create your models here.

class Label(BaseModel, HasIDString):
    desc = models.CharField(max_length=260, null=True, blank=True)


class Instance(BaseModel, HasIDString):
    name = models.CharField(max_length=120)
    desc = models.CharField(max_length=260, null=True, blank=True)
    callback = models.CharField(max_length=120, null=True, blank=True)
    is_down = models.BooleanField(default=False)
    last_check = models.DateTimeField(default=timezone.now)
    today_report = models.IntegerField(default=0)

    icon = models.ForeignKey(Media, related_name="instances", on_delete=models.SET_NULL, null=True, blank=True)
    external_ico = models.CharField(max_length=150, null=True, blank=True)

    is_localize = models.BooleanField(default=False)
    boundaries = models.JSONField(null=True, blank=True)

    labels = models.ManyToManyField(Label, related_name="instances", blank=True)

    def generate_reports(self, is_down):
        with open("cities.json") as f:
            dataset = json.load(f)
            limit = random.randint(80, 150)
            ct = random.choices(dataset)[0]
            i = 0
            while i < limit:
                Report.objects.create(
                    instance=self,
                    is_down=is_down,
                    lat=ct.get("lat"),
                    log=ct.get("lng")
                )
                i = i + 1


class Report(BaseModel):
    instance = models.ForeignKey(
        Instance,
        related_name="reports",
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        related_name="reports",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    ip = models.CharField(max_length=50, null=True, blank=True)
    lat = models.CharField(max_length=50, null=True, blank=True)
    log = models.CharField(max_length=50, null=True, blank=True)

    is_down = models.BooleanField(default=False)
    content = models.CharField(max_length=500, null=True, blank=True)

    created = models.DateTimeField(default=timezone.now, db_index=True)
