from django.http import Http404 
from django.conf import settings
from videoflix_app.models import Video
import os
import glob

DOMAIN = getattr(settings, 'DOMAIN')
VIDEO_EXTRA_FILES = {
    "poster":"poster.jpg",
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
      

def delete_files_starting_with(source, file_postfix="_thumb"):
    # Construct the pattern to match files starting with the given prefix
    file_name, _ = os.path.splitext(source)
    file_name = os.path.basename(file_name)
    file_postfix = f"{file_name}" + f"{file_postfix}"

    pattern = os.path.join("media/videos/", f"{file_postfix}*")
    
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


def update_video_file(source,video_path, file_field_name):
    """Update video duration"""
    file_name = os.path.splitext(source)[0]
    poster = file_name + f"_{file_field_name.get("poster")}"
    video_file_hd360 = file_name + f"_{file_field_name.get("video_file_hd360")}"
    video_file_hd480 = file_name + f"_{file_field_name.get("video_file_hd480")}"
    video_file_hd720 = file_name + f"_{file_field_name.get("video_file_hd720")}"
    video_file_hd1080 = file_name + f"_{file_field_name.get("video_file_hd1080")}"
    poster_file = glob.glob(poster)
    video_file_hd360_file, video_file_hd480_file = glob.glob(video_file_hd360), glob.glob(video_file_hd480)
    video_file_hd720_file, video_file_hd1080_file = glob.glob(video_file_hd720), glob.glob(video_file_hd1080)
    video = Video.objects.filter(video_file=video_path).first()
    if video:
        if poster_file:
            video.poster = DOMAIN + poster_file[0]
        if video_file_hd360_file:
            video.video_file_hd360 = DOMAIN + video_file_hd360_file[0]
        if video_file_hd480_file:
            video.video_file_hd480 = DOMAIN + video_file_hd480_file[0]
        if video_file_hd720_file:
            video.video_file_hd720 = DOMAIN + video_file_hd720_file[0]
        if video_file_hd1080_file:
            video.video_file_hd1080 = DOMAIN + video_file_hd1080_file[0]
        video.save()
