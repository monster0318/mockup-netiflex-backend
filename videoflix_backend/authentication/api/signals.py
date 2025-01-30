from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
import os
from config.config_settings import *

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created,**kwargs):
    if created:  
        subject = "Welcome To Videoflix!"
        context = {
            "username": instance.username,
        }
        message = render_to_string("emails/welcome.html", context)

        from_email = MAIL_USERNAME
        recipient_list = [instance.email, MAIL_USERNAME]
        email_to_send = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list

        ) 

        email_to_send.content_subtype = "html"
        email_to_send.send()
    

