from django import 	forms
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, CustomUser, MessageForUpravnik, Temp2
import logging
from dal import autocomplete

from home.models import Papir

logger = logging.getLogger(__name__)


# see https://stackoverflow.com/questions/20833638/how-to-log-all-django-form-validation-errors

# class TempUserForm(forms.ModelForm):
# 	class Meta:
# 		model = TempUser
# 		fields = "__all__"

# class EmailVerifiedUserForm(forms.ModelForm):
# 	class Meta:
# 		model = EmailVerifiedUser
# 		fields = "__all__"

class Register1Form(forms.Form):
     name = forms.CharField(label='Tvoje ime', max_length=100)
     email = forms.EmailField()

class Register2Form(forms.Form):
    šifra = forms.CharField(max_length=10)

class Register3Form(forms.ModelForm):

	class Meta:
	    model = Temp2
	    fields = ['Grad', 'Opština', 'ulaz']

class CustomUserRegisterForm(UserCreationForm):

	class Meta:
		model = CustomUser
		fields = ['username', 'password1', 'password2', 'Ulica_i_broj', 'Broj_stana']

class SecretForm(forms.Form):
	secr = forms.IntegerField()


class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = CustomUser
		fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image', 'o_sebi']

class OceniUpravnikaForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['oceni_upravnika']
		widgets = {
		'oceni_upravnika': forms.NumberInput(attrs={'min':1, 'max':10})
		}

class PapirForm(forms.ModelForm):
	class Meta:
		model = Papir
		fields = ['kolicina', 'ulaz', 'cena']
		# widgets = {
		#     'ulaz':autocomplete.ModelSelect2(url='ulaz-autocomplete')
		# }

class MessageForUpravnikForm(forms.ModelForm):
	class Meta:
		model = MessageForUpravnik
		fields = '__all__'
		

