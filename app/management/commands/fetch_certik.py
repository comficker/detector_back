from django.core.management.base import BaseCommand
from utils.helpers import get_username
from django.contrib.auth.models import User
from app.models import Instance, Label
from media.models import Media
import requests


def fetch(page):
    re = requests.post(
        'https://www.certik.com/api/projects-list',
        json={
            "sort": {}, "filter": {}, "currentPage": page, "dataPerPage": 30
        },
        headers={
            "content-type": "text/plain;charset=UTF-8",
            "cookie": "_gcl_au=1.1.582263569.1665581864; _gid=GA1.2.1942990616.1665581864; hubspotutk=e620dd3e4e89c115f60275937a4bc499; drift_aid=2db39910-3612-4f2f-b8ca-d01cbe387aa5; driftt_aid=2db39910-3612-4f2f-b8ca-d01cbe387aa5; _hjSessionUser_2453311=eyJpZCI6IjliZjQ4MGVlLTMwODYtNTkzYS1iYjkxLTFlYjIxYzg3NGMwMCIsImNyZWF0ZWQiOjE2NjU1ODE4NzE1OTAsImV4aXN0aW5nIjp0cnVlfQ==; __hssrc=1; next-auth.csrf-token=c239bc138db964e8b26b404fef72e76e421298fa530bdfe7767352fec33225a7%7C0cb0a4a772d67e0e0ad0647f29580b00fc569f5a79a7aea804c7ae8c13383d42; next-auth.callback-url=https%3A%2F%2Fwww.certik.com; _ga=GA1.2.656588652.1665581864; _hjIncludedInSessionSample=0; _hjSession_2453311=eyJpZCI6IjY4OTkzNGRkLWNhMDItNGU4Yy04OTg2LWNhNDA2YTAzMzFmYiIsImNyZWF0ZWQiOjE2NjU2Nzc0MzQ5MzUsImluU2FtcGxlIjpmYWxzZX0=; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=0; drift_campaign_refresh=8b2691de-e01a-481f-b171-abadbc31e563; __hstc=55193076.e620dd3e4e89c115f60275937a4bc499.1665581881089.1665592562894.1665677435438.4; __hssc=55193076.1.1665677435438; _ga_MY83VE1Y5L=GS1.1.1665677432.6.0.1665677496.60.0.0",
            "origin": "https://www.certik.com",
            "referer": "https://www.certik.com/",
            "sec-ch-ua": '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "macOS",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
        }
    )
    for item in re.json().get("results"):
        name = item.get("name").strip()
        test = Instance.objects.filter(name=name).count()
        if test > 0:
            continue
        instance, is_created = Instance.objects.get_or_create(
            name=name,
            defaults={
                "id_string": item.get("externalId"),
                "desc": item.get("description")[:259] if item.get("description") else None,
                "callback": item.get("website"),
                "external_ico": "https://certik-project-logos.imgix.net/{}".format(item.get("logo")),
                "socials": {
                    "twitter": item.get("twitter"),
                    "discord": item.get("discord")
                },
                "score": {
                    "securityScore": item.get("securityScore"),
                    "trustScore": item.get("trustScore"),
                    "communityMarketScore": item.get("communityMarketScore")
                }
            }
        )
        if is_created:
            for label in item.get("labels", []):
                l, _ = Label.objects.get_or_create(name=label)
                instance.labels.add(l)
            if item.get("logo"):
                media = Media.objects.save_url(
                    "https://certik-project-logos.imgix.net/{}".format(item.get("logo"))
                )
                if media:
                    instance.icon = media
                    instance.save()
            print(item.get("name"))
    fetch(page + 1)


class Command(BaseCommand):
    def handle(self, *args, **options):
        fetch(1)
