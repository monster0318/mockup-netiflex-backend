from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Video
from import_export import resources








class VideoResource(resources.ModelResource):

    class Meta:
        model = Video

@admin.register(Video)
class VideoAdmin(ImportExportModelAdmin):
    resource_classes = [VideoResource]
