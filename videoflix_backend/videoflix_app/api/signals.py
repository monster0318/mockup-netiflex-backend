from django.dispatch import receiver
from videoflix_app.models import Video
from django.db.models.signals import post_save, post_delete
import os
from videoflix_app.api.tasks import convert_to_format, create_vtt_file
import django_rq
from videoflix_app.api.utils import delete_files_starting_with
import json

@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created,**kwargs):

    source = os.path.join('media/', instance.video_file.name)
    if created:
        convert_to_format(source=source, quality='hd360')
        convert_to_format(source=source, quality='hd480')
        convert_to_format(source=source, quality='hd720')
        convert_to_format(source=source, quality='hd1080')
        create_vtt_file(source=source)
        queue = django_rq.get_queue('default',autocommit=True)
        # queue.enqueue(convert_to_format,source, "hd480")
        # queue.enqueue(create_vtt_file,source)


@receiver(post_delete, sender = Video)
def delete_video_on_file_delete(sender, instance, **kwargs):
    """Deleting video automatically when file is deleted"""
    
    source = os.path.join('media/', instance.video_file.name)

    delete_files_starting_with(source=source, file_postfix="_") 
    delete_files_starting_with(source=source, file_postfix="-") 
    delete_files_starting_with(source=source, file_postfix="") 
