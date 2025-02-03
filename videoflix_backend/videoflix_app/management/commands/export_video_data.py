from django.core.management.base import BaseCommand
from videoflix_app.admin import VideoResource
import datetime


class Command(BaseCommand):
    help = 'Export video data to JSON'

    def handle(self, *args, **kwargs):
        video_resource = VideoResource().export()
        exported_data = video_resource.json
        with open(f"exports/video_data_{datetime.datetime.today().isoformat()}.json", "w") as file:
            file.write(exported_data)
