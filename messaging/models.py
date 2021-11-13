from django.db import models
from users.models import CustomUser

# Create your models here.
# class Message(models.Model):
#     sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name= "sender")
#     receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="receiver")
#     Naslov = models.CharField(max_length=100)
#     Sadržaj = models.TextField()

class MessageForUpravnik(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="message_sender", null=True)
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="message_receiver", null=True)
    title = models.CharField(max_length=200, null=True)
    content = models.TextField(null=True)
    seen = models.BooleanField(default=False)
    read = models.BooleanField(default=False)


class MessageNotificationsBucket(models.Model):
    empty = models.BooleanField(default=True)