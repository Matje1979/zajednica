from django.urls import path
from .views import (MngrMessageListView,
	MsgDetailView,
	MsgDeleteView,
	CheckMessagesView,
	MessageListView
)
urlpatterns = [
    path('manager_messages/<int:pk>', MngrMessageListView.as_view(), name="mngr-messages"),
    path('messages/<int:pk>', MsgDetailView.as_view(), name="msg-detail"),
    path('messages/<int:pk>/delete', MsgDeleteView.as_view(), name="msg-delete"),
    path('check_messages/<str:pk>', CheckMessagesView.as_view(), name='check-messages'),
    path('messages_list/', MessageListView.as_view(), name='message-list')
]