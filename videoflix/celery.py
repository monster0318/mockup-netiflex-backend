import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE","videoflix.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

import configurations
configurations.setup()


app = Celery("videoflix")
app.config_from_object("django.conf:settings",namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from videoflix_app.api.utils import set_up_export_db_data
@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Runs when Celery starts"""
    set_up_export_db_data()