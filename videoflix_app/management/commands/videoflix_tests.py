from django.core.management.base import BaseCommand
from videoflix_app.admin import VideoResource
import subprocess


class Command(BaseCommand):
    help = 'Run all test inside the API'

    def handle(self, *args, **options):
        erase_cov = ["coverage", "erase"]
        test_api = ['pytest', '--cov=.', '--cov-report=term-missing', '--cov-report=html', '-s', '--verbose', '--color=yes']
        subprocess.run(erase_cov, capture_output=True,check=True)
        try:
            result_test = subprocess.run(test_api, check=True, text=True)
            print("Test output:", result_test.stdout)
        except subprocess.CalledProcessError as e:
            print("Error during pytest execution:", e.stderr)
        
