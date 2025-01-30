from django.dispatch import receiver
from videoflix_app.models import Video
from django.db.models.signals import post_save, post_delete
import os
from videoflix_app.api.tasks import convert_to_format


@receiver(post_save, sender=Video)
def video_post_save(sender, instance, created,**kwargs):
    output_file_name = instance.video_file.name.split('.')[0] + "_hd480.mp4" # Name of the uploaded file without extension 
    target = os.path.join('media/', output_file_name)  
    if created:
        convert_to_format(source=instance.video_file.path, target=target,format='hd480')
        print('Video successfully saved')


@receiver(post_delete, sender = Video)
def delete_video_on_file_delete(sender, instance, **kwargs):
    """Deleting video automatically when file is deleted"""

    if instance.video_file:
        if os.path.isfile(instance.video_file.path):
            os.remove(instance.video_file.path)