from django.db import models
from account.models import Profile
# Create your models here.
class Topic(models.Model):
    content=models.CharField(max_length=200)
    user=models.ForeignKey(Profile,on_delete=models.CASCADE)
    date_time=models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s/%s" % (self.content,self.user)
