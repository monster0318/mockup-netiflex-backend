from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    """Class represents a user"""
    phone = models.CharField(max_length=100,blank=True, null=True)
    address = models.TextField(max_length=250, blank=True, null=True)

    def to_dict(self):
        """Converting user data to dictionary"""
        return {
            "username" : self.username,
            "email" : self.email,
            "phone" : self.phone,
            "address" : self.address
        }
