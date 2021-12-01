from django.urls import path
from . import views

urlpatterns = [
    path("events/", views.events_home, name="event-list"),
]