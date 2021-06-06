from rest_framework import serializers
from users.models import TempPapir, Profile, Ulaz, TempCepovi, MessageForUpravnik
from .models import Papir, Cepovi
from drf_extra_fields.fields import Base64ImageField

class MessageForUpravnikSerializer(serializers.ModelSerializer):
	class Meta:
		model = MessageForUpravnik
		# fields = ('ulaz', 'foto') # or fields = '__all__'
		fields = '__all__'

class TempPapirSerializer(serializers.ModelSerializer):
	class Meta:
		model = TempPapir
		# fields = ('ulaz', 'foto') # or fields = '__all__'
		fields = '__all__'

class UlazSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ulaz
		# fields = ('ulaz', 'foto') # or fields = '__all__'
		fields = '__all__'

class PapirPrijavaSerializer(serializers.ModelSerializer):
    ulaz = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TempPapir
        fields = ('foto','ulaz') # or fields = '__all__'
# 		fields = '__all__'

class CepPrijavaSerializer(serializers.ModelSerializer):
    ulaz = serializers.PrimaryKeyRelatedField(read_only=True)
    foto = Base64ImageField()

    class Meta:
        model = TempCepovi
        fields = ('foto','ulaz', 'cep_box_filled_date') # or fields = '__all__'
# 		fields = '__all__'
    def create(self, validated_data):
        foto=validated_data.pop('foto')
        ulaz=validated_data.pop('ulaz')
        return TempCepovi.objects.create(ulaz=ulaz,foto=foto)

class PapirSerializer(serializers.ModelSerializer):
    ulaz = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Papir
        fields = ('kolicina','ulaz', 'datum', 'cena')

class CepoviSerializer(serializers.ModelSerializer):
    ulaz = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Cepovi
        fields = ('ulaz', 'datum')

class TempCepoviSerializer(serializers.ModelSerializer):
    ulaz = serializers.PrimaryKeyRelatedField(read_only=True)
    address = serializers.SerializerMethodField()
    class Meta:
        model = TempCepovi
        fields = ('ulaz', 'foto', 'address', 'cep_box_filled_date')
# 		fields = '__all__'

    def get_address(self, obj):
        return obj.ulaz.Ulica_i_broj
