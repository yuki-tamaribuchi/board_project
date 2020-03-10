from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    handle = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    biograph = models.CharField(max_length=200)

    def __str__(self):
        return user