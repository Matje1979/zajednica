from django.db import models

# Create your models here.


class PhoneCategory(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=80, null=True, blank=True)

    def __str__(self):
        return self.name

class PhoneNumber(models.Model):
    num = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    category = models.ForeignKey(PhoneCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name





