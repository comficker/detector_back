import random
import json
from django.db import models
from base.interface import BaseModel, HasIDString
from django.contrib.auth.models import User
from media.models import Media
from django.utils import timezone
from datetime import timedelta


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
    rp = models.JSONField(null=True, blank=True)

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

    def generate_rp(self):
        now = timezone.now()
        now.replace(hour=0, second=0, minute=0)
        before30 = now + timedelta(days=-30)
        if self.rp is None:
            self.rp = {}
        for report in self.reports.filter(created__gt=before30).order_by("created"):
            key = report.created.date().__str__()
            if not self.rp.get(key):
                self.rp[key] = {
                    "date": key,
                    "up": 0,
                    "down": 0
                }
            if report.is_down:
                self.rp[key]["down"] = self.rp[key]["down"] + 1
            else:
                self.rp[key]["up"] = self.rp[key]["up"] + 1
        if not (
                self.last_check.year == now.year and
                self.last_check.month == now.month and
                self.last_check.day == now.year):
            self.today_report = 0
        self.today_report = self.today_report + 1
        self.last_check = now
        self.save()


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
