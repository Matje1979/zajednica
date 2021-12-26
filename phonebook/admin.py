from django.contrib import admin
from .models import PhoneNumber, PhoneCategory

# Register your models here.
admin.site.register(PhoneNumber)
admin.site.register(PhoneCategory)