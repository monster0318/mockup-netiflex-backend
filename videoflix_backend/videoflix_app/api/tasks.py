import subprocess
import os

def convert_to_format(source):
    """Convert video to format {360,480,720,1080}"""
    file_name, _ = os.path.splitext(source)
    target = file_name + '_480p.mp4'
    if os.name == "nt":
        source = source.replace("\\","/").replace("C:","/mnt/c")

    converted_video = f'ffmpeg -i "{source}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{target}"'
    subprocess.run(converted_video,capture_output=True,shell=True)


def convert_mp4_to_m3u8(source):
    """Convert video from format mp4 to format m3u8"""
    file_name, _ = os.path.splitext(source)
    target = file_name + '_480p.m3u8'
    if os.name == "nt":
        source = source.replace("\\","/").replace("C:","/mnt/c")
        
    converted_video = f'ffmpeg -i {source} -codec: copy -start_number 0 -hls_time 10 -hls_list_size 0 -f hls {target}'
    subprocess.run(converted_video,capture_output=True,shell=True)


# convert_mp4_to_m3u8("media/videos/nature.mp4")