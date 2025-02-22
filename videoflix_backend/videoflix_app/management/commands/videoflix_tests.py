from django.core.management.base import BaseCommand
from videoflix_app.admin import VideoResource
import subprocess


class Command(BaseCommand):
    help = 'Run all test inside the API'

    def handle(self, *args, **options):
        test_api = "pytest --cov=. --cov-report=term-missing -s --verbose --color=yes"
        subprocess.run(test_api)
        
