from django.dispatch import receiver
from videoflix_app.models import Video
from django.db.models.signals import post_save, post_delete
import os
from videoflix_app.api.tasks import convert_to_format, convert_mp4_to_m3u8
import django_rq


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created,**kwargs):
 
    if created:
        convert_mp4_to_m3u8(source=instance.video_file.path)
        # queue = django_rq.get_queue('default',autocommit=True)
        # queue.enqueue(convert_to_format,instance.video_file.path)
        print('Video successfully saved')


@receiver(post_delete, sender = Video)
def delete_video_on_file_delete(sender, instance, **kwargs):
    """Deleting video automatically when file is deleted"""

    output_file_name = instance.video_file.name.split('.')[0] + "_hd480.mp4"
    target = os.path.join('media/', output_file_name)  
    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path) #remove original video
        if os.path.isfile(target):
            os.remove(target) #remove converted video