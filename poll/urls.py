from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('poll_home/', views.home, name="poll-home"),
    path('create/', views.create, name="poll-create"),
    path('vote/', views.vote, name="poll-vote"),
    path('results/', views.results, name="poll-results"),
]