from django.db import models
from django.contrib.auth.models import User

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