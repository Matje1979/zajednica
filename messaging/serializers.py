from rest_framework import serializers
from .models import MessageForUpravnik
# from drf_extra_fields.fields import Base64ImageField

class MessageForUpravnikSerializer(serializers.ModelSerializer):
	class Meta:
		model = MessageForUpravnik
		# fields = ('ulaz', 'foto') # or fields = '__all__'
		fields = '__all__'