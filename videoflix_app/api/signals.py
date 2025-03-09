from django.dispatch import receiver
from videoflix_app.models import Video
from django.db.models.signals import post_save, post_delete
from videoflix_app.api.tasks import convert_to_format, create_vtt_file, update_video_duration, update_video_file
from celery.exceptions import TimeoutError
from videoflix_app.api.utils import delete_files_starting_with, VIDEO_EXTRA_FILES
from celery import chain
import os
import logging


logger = logging.getLogger(__name__)


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created,**kwargs):
    """Generate different video qualities after video upload"""
    source = os.path.join('media/', instance.video_file.name)

    if created:
        update_video_duration(source=source, video_path=instance.video_file.name)
        try:      
            workflow = chain(
                convert_to_format.s(source, ['hd360', 'hd480', 'hd720', 'hd1080']),
                create_vtt_file.si(source),
                update_video_file.si(source, instance.video_file.name, VIDEO_EXTRA_FILES) 
            )

            result = workflow.apply_async()
            result.get(timeout=5) 
        except TimeoutError:
            logger.info("The upload process is running ...")


@receiver(post_delete, sender = Video)
def delete_video_on_file_delete(sender, instance, **kwargs):
    """Deleting video automatically when file is deleted"""
    
    source = os.path.join('media/', instance.video_file.name)
    delete_files_starting_with(source=source, file_suffixes=["_","-",""]) 



