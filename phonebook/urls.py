from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    path("phonebook/", views.phoneslist, name="app-phonebook"),
    path("phone_numbers/<int:pk>", views.get_phone_numbers, name="app-get-phones"),
]
