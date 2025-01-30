from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    video_file = models.FileField(upload_to='videos',blank=True,null=True)


    def __str__(self):
        return self.title
