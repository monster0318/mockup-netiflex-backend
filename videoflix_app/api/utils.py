import json
from django.http import Http404 
from django_celery_beat.models import CrontabSchedule, PeriodicTask
import os
import glob


VIDEO_EXTRA_FILES = {
    "poster":"poster.jpg",
    "vtt_file":".vtt",
    "video_file_hd360":"hd360.mp4",
    "video_file_hd480":"hd480.mp4",
    "video_file_hd720":"hd720.mp4",
    "video_file_hd1080":"hd1080.mp4",
}


def get_or_404(model,pk):
    """Get model object or return 404 Not Found"""

    try:
        pk = int(pk)
        instance = model.objects.get(pk=pk)
        return instance
    except ValueError:
        raise ValueError("The ID must be an integer")
    except model.DoesNotExist:
        raise Http404("Model does not exist")
      

def delete_files_starting_with(source, file_suffixes=["_thumb"]):
    # Construct the pattern to match files starting with the given prefix
    file_name, _ = os.path.splitext(source)
    file_name = os.path.basename(file_name)

    for file_suffix in file_suffixes:
        file_suffix = f"{file_name}" + f"{file_suffix}"
        pattern = os.path.join("media/videos/", f"{file_suffix}*")
        
        files_to_delete = glob.glob(pattern)
        if files_to_delete:
            for file in files_to_delete:
                try:
                    os.remove(file)
                except Exception as e:
                    print(f"Error deleting {file}: {e}")


def seconds_to_time(seconds):
    """Convert time in string"""

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    if hours > 0:
        return f"{hours:02}:{minutes:02}:{remaining_seconds:02}"
    else:
        return f"{minutes:02}:{remaining_seconds:02}"


def set_up_export_db_data():
    """Export video data from database """

    schedule, created = CrontabSchedule.objects.get_or_create(minute="0", hour="6",day_of_week='sunday')
    args = json.dumps([])
    periodic_task, created = PeriodicTask.objects.get_or_create(
            name = 'Database periodic backup',
            crontab = schedule,
            args = args,
            task = "videoflix_app.api.tasks.export_db_data"
    )
