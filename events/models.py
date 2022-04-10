from django.db import models

from users.models import CustomUser

# Create your models here.


class Event(models.Model):
    name = models.CharField(max_length=50)
    start = models.DateTimeField()
    end = models.DateTimeField()
    location = models.CharField(max_length=50)
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
