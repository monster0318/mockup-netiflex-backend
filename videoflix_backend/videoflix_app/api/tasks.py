import subprocess

def convert_to_format(source, target, format):
    """Convert video to format {360,480,720,1080}"""
    converted_video = f'ffmpeg -i "{source}" -s {format} -c:v libx264 -crf 23 -c:a aac -strict -2 "{target}"'
    subprocess.run(converted_video)
