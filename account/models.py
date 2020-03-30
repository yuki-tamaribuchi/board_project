from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    handle = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    biograph = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username


class Follow(models.Model):
    following_user=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='following_user')
    followed_user=models.ForeignKey(Profile,on_delete=models.CASCADE,related_name='followed_user')

    def __str__(self):
        return '%s is following %s' % (self.following_user,self.followed_user)


class Notification(models.Model):
    TYPES=(
        ('FL','Followed'),
        ('RE','Replied'),
        ('LI','Liked'),
    )

    user=models.ForeignKey(User,on_delete=models.CASCADE)
    notify_type=models.CharField(max_length=2,choices=TYPES)
    content=models.CharField(max_length=100)
    recieved_time=models.DateTimeField(auto_now=timezone.now)