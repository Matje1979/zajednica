from django.db import models
from users.models import CustomUser

# Create your models here.

class Poll(models.Model):
	author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
	question = models.TextField()
	option_one = models.CharField(max_length=30)
	option_two = models.CharField(max_length=30)
	option_three = models.CharField(max_length=30, null=True, blank=True)
	ption_one_count = models.IntegerField(default=0)
	ption_one_count = models.IntegerField(default=0)
	ption_one_count = models.IntegerField(default=0)
