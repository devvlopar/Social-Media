import email
from django.db import models

# Create your models here.

class User(models.Model):
    fullname = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    bio = models.CharField(max_length=60, null=True, blank=True)
    location = models.CharField(max_length=20, null=True, blank=True)
    profession = models.CharField(max_length=20, null=True, blank=True)
    pic = models.FileField(upload_to='profile',default='avtar.png')
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)

    

    def __str__(self):
        return self.fullname
