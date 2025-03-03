from videoflix_app.api.utils import delete_files_starting_with, seconds_to_time
from videoflix_app.models import Video
from videoflix_app.admin import VideoResource
from django.conf import settings
from celery import shared_task
import subprocess
import glob
import os
import json
import datetime
import math  
from celery import Task
from django_celery_results.models import TaskResult


DOMAIN = getattr(settings, 'DOMAIN')

class CustomTask(Task):
    def on_success(self, retval, task_id, args, kwargs):
        """Automatically set the task name in TaskResult"""
        task_result = TaskResult.objects.filter(task_id=task_id).first()
        if task_result:
            task_result.task_name = self.name
            task_result.save()
        super().on_success(retval, task_id, args, kwargs)

def has_audio_stream(source):
    """Use ffprobe to check if the source file contains an audio stream."""
    cmd = [
        "ffprobe",
        "-v", "error",
        "-select_streams", "a",
        "-show_entries", "stream=index",
        "-of", "json",
        source
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    try:
        info = json.loads(result.stdout)
        streams = info.get("streams", [])
        return len(streams) > 0
    except Exception:
        return False

def convert_to_format_m3u8(source, qualities):
    """
    Convert video to an HLS stream with two quality variants: 480p and 720p.
    This generates a master playlist (master.m3u8) that references the two variant playlists.
    """
    # Ensure qualities is a list and contains both 480 and 720 (as strings for comparison)
    if not qualities or not isinstance(qualities, list):
        return
    required = {"480", "720"}
    provided = {str(q) for q in qualities}
    if not required.issubset(provided):
        # If both qualities are not requested, you can decide to add defaults or return.
        return

    # Get the file name without extension
    file_name, _ = os.path.splitext(source)
    # If running on Windows, adjust path for WSL (as in your original function)
    if os.name == "nt":
        source = source.replace("\\", "/").replace("C:", "/mnt/c")
        file_name = file_name.replace("\\", "/").replace("C:", "/mnt/c")

    audio_exists = has_audio_stream(source)

    # Build the FFmpeg command based on whether audio exists
    if audio_exists:
        # Build command including audio mapping
        ffmpeg_command = (
            f'ffmpeg -i "{source}" '
            f'-filter_complex "[0:v]split=2[v720][v480]" '
            f'-map "[v720]" -c:v:0 libx264 -b:v:0 2500k -s:v:0 1280x720 '
            f'-map 0:a -c:a aac -b:a:0 128k '
            f'-map "[v480]" -c:v:1 libx264 -b:v:1 1000k -s:v:1 854x480 '
            f'-map 0:a -c:a aac -b:a:1 96k '
            f'-f hls -hls_time 4 -hls_playlist_type vod '
            f'-var_stream_map "v:0,a:0 v:1,a:1" '
            f'-master_pl_name master.m3u8 '
            f'-hls_segment_filename "{file_name}_%v_%03d.ts" '
            f'"{file_name}_%v.m3u8"'
        )
    else:
        # Build command without audio mapping
        ffmpeg_command = (
            f'ffmpeg -i "{source}" '
            f'-filter_complex "[0:v]split=2[v720][v480]" '
            f'-map "[v720]" -c:v:0 libx264 -b:v:0 2500k -s:v:0 1280x720 '
            f'-map "[v480]" -c:v:1 libx264 -b:v:1 1000k -s:v:1 854x480 '
            f'-f hls -hls_time 4 -hls_playlist_type vod '
            f'-var_stream_map "v:0 v:1" '
            f'-master_pl_name master.m3u8 '
            f'-hls_segment_filename "{file_name}_%v_%03d.ts" '
            f'"{file_name}_%v.m3u8"'
        )

    resp=subprocess.run(ffmpeg_command, capture_output=True, shell=True,text=True)
    if resp.returncode !=0:
        print('error happen',resp.stderr)
    else:
        print('success')

@shared_task(name="Generate-video-qualities", base=CustomTask)
def convert_to_format(source,qualities):
    """Convert video to format {360,120,720,1080}"""
    if not qualities or not isinstance(qualities,list):
        return
    for quality in qualities:
        file_name, _ = os.path.splitext(source)
        target = file_name + f'_{quality}.mp4'
        if os.name == "nt":
            source = source.replace("\\","/").replace("C:","/mnt/c")
            target = target.replace("\\","/").replace("C:","/mnt/c")
        
        converted_video = f'ffmpeg -i "{source}" -s {quality} -c:v libx264 -crf 23 -c:a aac -strict -2 "{target}"'
        subprocess.run(converted_video,capture_output=True,shell=True)

def generate_thumbnails(source, thumb_width):
    """Generate the thumbnails files"""
    source = os.path.abspath(source)
    file_name, _ = os.path.splitext(source)
    output_pattern = f"{file_name}_thumb%05d.jpg"

    if os.name == "nt":
        source = source.replace("\\", "/").replace("C:", "/mnt/c")
        output_pattern = output_pattern.replace("\\", "/").replace("C:", "/mnt/c")

    command = [
        "ffmpeg", "-i", source, "-vf", f"fps=1,scale={thumb_width}:-1", output_pattern
    ]

    subprocess.run(command, text=True, capture_output=True)

def generate_video_poster(source, video_duration):
    """Generate a poster for the video"""
    source = os.path.abspath(source)
    file_name, _ = os.path.splitext(source)
    output_path = f"{file_name}_poster.jpg"

    if video_duration>=60:
        video_duration = 10
    timestamp = "00:" + seconds_to_time(video_duration)

    if os.name == "nt":
        source = source.replace("\\", "/").replace("C:", "/mnt/c")
        output_path = output_path.replace("\\", "/").replace("C:", "/mnt/c")
    command = [
        "ffmpeg","-i", source, "-ss", timestamp,"-vframes", "1","-q:v", "2", output_path        
    ]
    subprocess.run(command, capture_output=True, text=True)

def generate_sprite(source):
    """Generate sprite from the thumbnails dynamically adjusting tile size"""
    source = os.path.abspath(source)
    file_name, _ = os.path.splitext(source)
    source_folder = os.path.dirname(source)
    file_base_name = os.path.basename(file_name)

    # Get all thumbnail images
    thumbnails = glob.glob(os.path.join(source_folder, f"{file_base_name}_thumb*.jpg"))

    if not thumbnails:
        return

    num_thumbnails = len(thumbnails)
    cols = math.ceil(math.sqrt(num_thumbnails))  
    rows = math.ceil(num_thumbnails / cols)    

    print(f"Generating sprite with {num_thumbnails} images in a {cols}x{rows} grid.")
 
    target = os.path.join(source_folder, f"{file_base_name}.jpg")

    if os.name == "nt":
        source_folder = source_folder.replace("\\", "/")
        target = target.replace("\\", "/")

    command = ["montage"] + thumbnails + ["-tile", f"{cols}x{rows}", "-geometry", "+0+0", target]
    subprocess.run(command, text=True, capture_output=True)
    return cols

def get_video_duration(source):
    """Get the duration of the video using"""
    command = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", source
    ]
    result = subprocess.run(command, text=True, capture_output=True)
    if result.returncode != 0:
        return 0
    return int(float(result.stdout.strip()))

def update_video_duration(source,video_path):
    """Update video duration"""
    try:
        video = Video.objects.filter(video_file=video_path).first()
        duration = get_video_duration(source)
        video.duration = seconds_to_time(duration)
        video.save()
        return 1
    except Video.DoesNotExist:
        print("Video does not exist")
        return 0
    
def generate_vtt(sprite_file, num_thumbnails, cols, thumb_width=320, thumb_height=180):
    """Generate vtt file from the sprites to be used in plyr"""
    vtt_file = os.path.splitext(sprite_file)[0] + ".vtt"
    vtt_file = os.path.join("media/videos/", vtt_file)
    with open(vtt_file, "w") as f:
        f.write("WEBVTT\n\n")  
        
        for i in range(num_thumbnails):
            start_time = f"00:{i:02}.000"  
            end_time = f"00:{i+1:02}.000"  
            
            x = (i % cols) * thumb_width
            y = (i // cols) * thumb_height
            
            f.write(f"{start_time} --> {end_time}\n")
            f.write(f"{sprite_file}#xywh={x},{y},{thumb_width},{thumb_height}\n\n")

@shared_task(name="Create-VTT-file", base=CustomTask)
def create_vtt_file(source):
        """Creating the VTT file and removing the unused files"""
        file_name, _ = os.path.splitext(source)
        sprite_file_name = os.path.basename(file_name)
        video_duration = get_video_duration(source=source)
        generate_thumbnails(source=source, thumb_width=320)
        generate_video_poster(source=source, video_duration=int(0.5*video_duration))
        cols = generate_sprite(source=source)
        generate_vtt(f"{sprite_file_name}.jpg", num_thumbnails=video_duration, cols=cols, thumb_width=320, thumb_height=180)
        delete_files_starting_with(source=source)

@shared_task(name="Update-video-quality-links", base=CustomTask)
def update_video_file(source,video_path, file_field_name):
    """Update video duration"""
    file_name = os.path.splitext(source)[0]
    poster = file_name + f"_{file_field_name.get("poster")}"
    vtt_file = file_name + f"{file_field_name.get("vtt_file")}"
    video_file_hd360 = file_name + f"_{file_field_name.get("video_file_hd360")}"
    video_file_hd480 = file_name + f"_{file_field_name.get("video_file_hd480")}"
    video_file_hd720 = file_name + f"_{file_field_name.get("video_file_hd720")}"
    video_file_hd1080 = file_name + f"_{file_field_name.get("video_file_hd1080")}"
    poster_file, vtt_file = glob.glob(poster), glob.glob(vtt_file)
    video_file_hd360_file, video_file_hd480_file = glob.glob(video_file_hd360), glob.glob(video_file_hd480)
    video_file_hd720_file, video_file_hd1080_file = glob.glob(video_file_hd720), glob.glob(video_file_hd1080)
    video = Video.objects.filter(video_file=video_path).first()
    if video:
        if poster_file:
            video.poster = DOMAIN + poster_file[0]
        if vtt_file:
            video.vtt_file = DOMAIN + vtt_file[0]
        if video_file_hd360_file:
            video.video_file_hd360 = DOMAIN + video_file_hd360_file[0]
        if video_file_hd480_file:
            video.video_file_hd480 = DOMAIN + video_file_hd480_file[0]
        if video_file_hd720_file:
            video.video_file_hd720 = DOMAIN + video_file_hd720_file[0]
        if video_file_hd1080_file:
            video.video_file_hd1080 = DOMAIN + video_file_hd1080_file[0]
        video.save()


@shared_task(name='Export-DB-data-for-backup', base=CustomTask)
def export_db_data():
    dataset = VideoResource().export()
    with open(f"exports/video_data_{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.json")}", "w") as file:
        file.write(dataset.json)