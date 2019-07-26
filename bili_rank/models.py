from django.db import models, migrations
from django.utils import timezone

# Create your models here.

class User_info(models.Model):
    '''哔哩哔哩用户粉丝排行'''
    name = models.CharField(max_length=60)
    follower_count = models.PositiveIntegerField(default=0)
    uid = models.CharField(max_length=60)
    addfollower = models.IntegerField(default=-10000000) # 粉丝变化
    rank = models.PositiveIntegerField(default=0) 
    lastrank = models.IntegerField(default=-200) # 排名变化
    lastmodify = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
class Submits(models.Model):
    '''用户提交信息'''
    url = models.CharField(max_length=120)

    def __str__(self):
        return self.url

        
# #chang django field type
# class Migration(migrations.Migration):
#     operations = [
#         migrations.AlterField('User_info', 'lastrank', models.IntegerField(default=0))
#     ]