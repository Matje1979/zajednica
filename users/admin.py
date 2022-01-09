from django.contrib import admin
from .models import Profile, Ulaz, KomentarUpravnika
from .models import CustomUser, Upravnik, Temp, TempPapir, Grad, Opština
from .forms import CustomUserRegisterForm
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(Profile)

class CustomUserAdmin(UserAdmin):
	model = CustomUser

	add_form = CustomUserRegisterForm

	fieldsets = (
		*UserAdmin.fieldsets,
		(
			'User role',
			{
			    'fields': (
			    	'is_director',

			    )
			}

		),
		(
			'User Location',
		{
		    'fields': (
		    	'Grad',
		    	'Opština',
		    	'Ulica_i_broj',
		    	'Broj_stana',
		    	'Ulaz',
		    	)
		    }
        ),
        (
            'Likes',
            {
                'fields': (
                    'liked_posts',
                )
            }
        )

	)

admin.site.register(Grad)
admin.site.register(Opština)
admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(TempUser)
# admin.site.register(EmailVerifiedUser)
admin.site.register(Ulaz)
admin.site.register(Upravnik)
admin.site.register(KomentarUpravnika)
admin.site.register(Temp)
admin.site.register(TempPapir)