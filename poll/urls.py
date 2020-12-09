from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('poll_home/', views.home, name="poll-home"),
    path('create/', views.create, name="poll-create"),
    path('vote/<int:poll_id>', views.vote, name="poll-vote"),
    path('results/<int:poll_id>', views.results, name="poll-results"),
]