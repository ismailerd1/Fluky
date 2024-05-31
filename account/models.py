from django.db import models
from django.contrib.auth.models import User
import random
import string

# Create your models here.

def user_directory_path(instance, filename):
    # Profil resimlerini "media" klasörü altında "user_<user_id>" klasörlerinde sakla
    return f'user_{instance.user.id}/{filename}'



class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_bio = models.TextField(blank=True)
    user_tags = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(default='default_pp.jpg',upload_to=user_directory_path)
    
    def __str__(self):
        return str(self.user)


