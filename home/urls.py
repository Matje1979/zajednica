from django.urls import path
from .views import (
	PostListView, 
	PostDetailView, 
	PostCreateView,
	PostUpdateView,
	PostDeleteView
)
from . import views

urlpatterns = [
    path('home/', PostListView.as_view(), name="app-home"),
   
    path('', views.frontpage, name="app-frontpage"),
    path('post/<int:pk>', PostDetailView.as_view(), name="post-detail"),
    path('post/<int:pk>/update', PostUpdateView.as_view(), name="post-update"),
    path('post/<int:pk>/delete', PostDeleteView.as_view(), name="post-delete"),
    path('post/new/', PostCreateView.as_view(), name="post-create"),
    path('about/', views.about, name="app-about"),
    path('reciklaza/', views.reciklaza, name="app-reciklaza"),
    path('tag/<slug:slug>', views.tagged, name="app-tagged"),
    path('telefoni/', views.telefoni, name="app-telefoni"),
    path('telefoni_p/', views.telefoni_p, name="app-telefoni-public"),
    path('upravnik_postovi/<int:pk>', views.upravnik_posts, name='upravnik-posts'),
]