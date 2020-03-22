from django.db import models
from account.models import Profile
# Create your models here.
class Topic(models.Model):
    content=models.CharField(max_length=200)
    user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    date_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s/%s' % (self.content,self.user)

class Reply(models.Model):
    reply_to=models.ForeignKey(Topic,on_delete=models.CASCADE,related_name='reply_to')
    reply_from=models.ForeignKey(Topic,on_delete=models.CASCADE,related_name='reply_from')


    def __str__(self):
        return '%s to %s' % (self.reply_from,self.reply_to)