from django.urls import path
from . import views
from .views import (MngrMessageListView,
	MsgDetailView,
	MsgDeleteView,
	CheckMessagesView,
	MessageListView,
	SentMessagesView
)
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('manager_messages/<int:pk>', MngrMessageListView.as_view(), name="mngr-messages"),
    path('messages/<int:pk>', MsgDetailView.as_view(), name="msg-detail"),
    path('messages/<int:pk>/delete', MsgDeleteView.as_view(), name="msg-delete"),
    path('check_messages/<str:pk>', CheckMessagesView.as_view(), name='check-messages'),
    # path('mark_seen/<str:pk>', views.mark_seen, name='check-messages'),
    path('messages_list/', MessageListView.as_view(), name='message-list'),
    path('sent_messages/', SentMessagesView.as_view(), name='sent-messages'),
    path('create_message/', views.create_message, name='create-message'),
    path("mark_seen/<str:pk>", csrf_exempt(views.MarkSeenView.as_view())),
]