from django import 	forms
from django.forms.widgets import Select
# from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, CustomUser, Ulaz, Grad
import logging


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

# class Register3Form(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['ulaz'].queryset = Ulaz.objects.none()


#     class Meta:
# 	   # CHOICES=Grad.objects.all()
# 	   # choice_list = [(x.name, x.name) for x in CHOICES]
# 	   # first = ("----------","----------")
# 	   # choice_list.insert(0, first)
# 	    model = Temp2
# 	    fields = ['Grad', 'Opština', 'ulaz', 'Broj_stana']
# 	   # choices = tuple(choice_list)
# 	    widgets = {
# 	       # 'Grad': Select(choices=choices, initial="none"),
# 	        'Opština': Select()
# 	        }



class CustomUserRegisterForm(UserCreationForm):

	class Meta:
		model = CustomUser
		fields = ['username', 'password1', 'password2']

class SecretForm(forms.Form):
	secr = forms.IntegerField(label="Ovde upišite šifru koja vam je poslata na email adresu.")


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
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['kolicina'].required = True
		self.fields['ulaz'].required = True
		self.fields['ulaz'].queryset = Ulaz.objects.filter(papir_box_full=True)
		self.fields['cena'].required = True

	class Meta:
		model = Papir
		fields = ['kolicina', 'ulaz', 'cena']
		widgets = {
		'kolicina': forms.NumberInput(attrs={'min':1}),
		'cena': forms.NumberInput(attrs={'min':1})
		}
		# widgets = {
		#     'ulaz':autocomplete.ModelSelect2(url='ulaz-autocomplete')
		# }

# class MessageForUpravnikForm(forms.ModelForm):
# 	class Meta:
# 		model = MessageForUpravnik
# 		fields = ['title', 'content']
# 		labels={
# 		    'title': 'Naslov',
# 		    'content': 'Sadržaj'
# 		}


