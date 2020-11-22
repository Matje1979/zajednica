from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

VRSTE_UPRAVNIKA = (
    ("Upravnik - domaće lice", "Upravnik - domaće lice"),
    ("Profesionalni upravnik - domaće lice", "Profesionalni upravnik - domaće lice"),
)

class Ulaz(models.Model):
    Grad=models.CharField(max_length=50)
    Opština=models.CharField(max_length=50)
    Ulica_i_broj=models.CharField(max_length=100)

    def __str__(self):
        return str(self.Ulica_i_broj)

    class Meta:
        verbose_name_plural="Ulazi"


class CustomUser(AbstractUser):
    is_director= models.BooleanField(default=False)
    Grad=models.CharField(max_length=100)
    Opština=models.CharField(max_length=25)
    Ulica_i_broj=models.CharField(max_length=100)
    Broj_stana=models.CharField(max_length=25)
    Ulaz = models.ForeignKey(Ulaz, on_delete=models.CASCADE, null=True, blank=True)
    upravnik_id = models.CharField(max_length=25, null=True, blank=True)

    def __str__(self):
        return str(self.username)
 
class Upravnik(models.Model):
    ulaz=models.OneToOneField(Ulaz, on_delete=models.CASCADE, related_name="Ulaz")
    user=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vrsta=models.CharField(max_length=50, choices = VRSTE_UPRAVNIKA, default="Upravnik - domaće lice")
    firma=models.CharField(max_length=150, null=True, blank=True)
    website=models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return "Upravnik stambene zajednice " + str(self.ulaz)

    class Meta:
        verbose_name_plural="Upravnici"

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # is_director = models.BooleanField()
    image = models.ImageField(default='default.jpg', upload_to="profile_pics")
    o_sebi = models.TextField(null=True, blank=True)
    oceni_upravnika = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], null=True, blank=True)
    prosecna_ocena = models.FloatField(null=True, blank=True)
    is_director = models.BooleanField(default=False)
    radi_za = models.CharField(max_length=100, null=True, blank=True)
    vrsta_upravnika = models.CharField(max_length=100, null=True, blank=True)
    is_organisation = models.BooleanField(default=False)
    
    # ulaz = models.ForeignKey(Ulaz, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Temp(models.Model):
    secr = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)

class Temp2(models.Model):
    secr = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    Grad = models.CharField(max_length=50, null=True, blank=True)
    Opština = models.CharField(max_length=50, null=True, blank=True)
    ulaz = models.ForeignKey(Ulaz, on_delete=models.CASCADE)


# class UpravnikProfile(models.Model):
#     user = models.OneToOneField(UpravnikUser, on_delete=models.CASCADE)
#     image = models.ImageField(default='default.jpg', upload_to="profile_pics")
#     oceni_upravnika = models.IntegerField(null=True, blank=True)
#     prosecna_ocena = models.FloatField(null=True, blank=True)
#     is_director = models.BooleanField(default=False)
#     radi_za = models.CharField(max_length=100, null=True, blank=True)
#     vrsta_upravnika = models.CharField(max_length=100, null=True, blank=True)
#     o_sebi = models.TextField(null=True, blank=True)
#     is_organisation = models.BooleanField(default=False)
#     # ulaz = models.ForeignKey(Ulaz, on_delete=models.CASCADE, null=True, blank=True)
    
#     def __str__(self):
#         return f'{self.user.username} Profile'

#     def save(self, *args, **kwargs):
#         super(Profile, self).save(*args, **kwargs)

#         img = Image.open(self.image.path)

#         if img.height > 300 or img.width > 300:
#             output_size = (300, 300)
#             img.thumbnail(output_size)
#             img.save(self.image.path)

class KomentarUpravnika(models.Model):
    upravnik = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="upravnik_ulaza", null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    autor =models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="customuser", null=True, blank=True)

    class Meta:
        verbose_name_plural="Komentari upravnika"

class MessageForUpravnik(models.Model):
    title=models.CharField(max_length=200, null=True)
    content=models.TextField(null=True)

# class TempUser(models.Model): 
#     Email = models.EmailField(max_length=250)
#     Grad=models.CharField(max_length=100)
#     Opština=models.CharField(max_length=100)
#     Ulica=models.CharField(max_length=250)
#     Broj=models.CharField(max_length=25)
#     code=models.IntegerField()

# class EmailVerifiedUser(models.Model):
#     username = models.CharField(max_length=250)
#     password1=models.CharField(max_length=250)
#     password2=models.CharField(max_length=250)
#     email = models.EmailField(max_length=250)
#     Grad=models.CharField(max_length=100)
#     Opština=models.CharField(max_length=100)
#     Ulica=models.CharField(max_length=250)
#     Broj=models.CharField(max_length=25)
#     code=models.IntegerField()

