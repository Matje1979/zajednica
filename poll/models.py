from django.db import models
from users.models import CustomUser
from django.utils import timezone

# Create your models here.

class Poll(models.Model):
	author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, related_name='author')
	question = models.TextField()
	option_one = models.CharField(max_length=30, default='Da')
	option_two = models.CharField(max_length=30, default='Ne')
	option_three = models.CharField(max_length=30, default='Svejedno', blank=True)
	ption_one_count = models.IntegerField(default=0)
	ption_two_count = models.IntegerField(default=0)
	ption_three_count = models.IntegerField(default=0)
	voters = models.ManyToManyField(CustomUser)
	date_created = models.DateTimeField(default=timezone.now)

	def __str__(self):
		return self.question
