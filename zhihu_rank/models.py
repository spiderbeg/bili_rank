from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
	"""知乎用户id"""
	uid = models.CharField(max_length=60)
	name = models.CharField(max_length=60)

	def __str__(self):
		return self.name

class User_info(models.Model):
	"""
	知乎用户基本信息
		点赞数
		粉丝数
		回答数
		...
	"""
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	followerCount = models.PositiveIntegerField(default=0)
	# followingCount = models.PositiveIntegerField(default=0)
	# answerCount = models.PositiveIntegerField(default=0)
	# questionCount = models.PositiveIntegerField(default=0)
	# articlesCount = models.PositiveIntegerField(default=0)
	# favoriteCount = models.PositiveIntegerField(default=0)
	# favoritedCount = models.PositiveIntegerField(default=0)
	# voteupCount = models.PositiveIntegerField(default=0)
	# thankedCount = models.PositiveIntegerField(default=0)
	# includedAnswersCount = models.PositiveIntegerField(default=0)
	# includedArticlesCount = models.PositiveIntegerField(default=0)
	# followingTopicCount = models.PositiveIntegerField(default=0)
	# followingQuestionCount = models.PositiveIntegerField(default=0)
	# avatarUrl = models.CharField(max_length=120)
	modify = models.DateTimeField(default=timezone.now)
	rankchange = models.IntegerField(default=-200) # 排名变化
	rank = models.PositiveIntegerField(default=0) 
	followerchange = models.IntegerField(default=-10000000) # 粉丝变化

	def __str__(self):
		return self.user.name

class Submits(models.Model):
    '''用户提交信息'''
    url = models.CharField(max_length=120)

    def __str__(self):
        return self.url