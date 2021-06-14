from django import 	forms
from .models import MessageForUpravnik

class MessageReplyForm(forms.ModelForm):
    class Meta:
        model = MessageForUpravnik
        fields = ['title', 'content']

class MessageForUpravnikForm(forms.ModelForm):
	class Meta:
		model = MessageForUpravnik
		fields = ['title', 'content']
		labels={
		    'title': 'Naslov',
		    'content': 'Sadržaj'
		}