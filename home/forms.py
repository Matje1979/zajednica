from django import forms
from.models import Comment
# from users.models import MessageForUpravnik


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']


# class MessageReplyForm(forms.ModelForm):
#     class Meta:
#         model = MessageForUpravnik
#         fields = ['title', 'content']
