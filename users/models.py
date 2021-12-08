# -*- coding: utf-8 -*-
from django.db import models
from django.apps import apps

from PIL import Image
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import ugettext_lazy as _
from location_field.models.plain import PlainLocationField



# Create your models here.

VRSTE_UPRAVNIKA = (
    ("Upravnik - domaće lice", "Upravnik - domaće lice"),
    (
        "Profesionalni upravnik - domaće lice",
        "Profesionalni upravnik - domaće lice"
    ),
)


class Grad(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Gradovi"


class Opština(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    Grad = models.ForeignKey(
        Grad, on_delete=models.CASCADE, related_name="opštine"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Opštine"


class Ulaz(models.Model):
    Grad = models.ForeignKey(
        Grad, on_delete=models.SET_NULL, related_name="ulazi", null=True
    )
    Opština = models.ForeignKey(
        Opština, on_delete=models.SET_NULL, related_name="ulazi", null=True
    )
    Ulica_i_broj = models.CharField(max_length=100)
    website = models.URLField(default="https://www.b92.net/")
    papir_box_full = models.BooleanField(default=False)
    cep_box_full = models.BooleanField(default=False)
    cep_box_filled_date = models.FloatField(null=True, blank=True)
    city = models.CharField(max_length=255, default='Belgrade')
    location = PlainLocationField(
        based_fields=['city'], zoom=10, null=True, blank=True
    )

    def __str__(self):
        return str(self.Ulica_i_broj)

    class Meta:
        verbose_name_plural = "Ulazi"


class MyValidator(UnicodeUsernameValidator):
    regex = r'^[\w.@+\- ]+$'


class CustomUser(AbstractUser):
    username_validator = MyValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_(
            'Required. 150 characters or fewer.'
            'Letters, digits and @/./ /-/_ only.'
        ),
        validators=[username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    is_director = models.BooleanField(default=False)
    Grad = models.CharField(max_length=100)
    Opština = models.CharField(max_length=25)
    Ulica_i_broj = models.CharField(max_length=100)
    Broj_stana = models.CharField(max_length=25)
    Ulaz = models.ForeignKey(
        Ulaz, on_delete=models.CASCADE, null=True, blank=True
    )
    upravnik_id = models.CharField(max_length=25, null=True, blank=True)
    liked_posts = models.ManyToManyField("home.Post", related_name="user_likes")

    def __str__(self):
        return str(self.username)

    def toggle_post_like(self, post_id):
        print("Hey you!", flush=True)
        """
        Add post to liked_posts if post is not in liked_posts
        and remove it if it is."""
        Post = apps.get_model('home', 'Post')
        post = Post.objects.get(id=post_id)
        print("Post", post, flush=True)
        if post in self.liked_posts.all():
            print("Post in liked posts", flush=True)
            try:
                self.liked_posts.remove(post)
            except Exception as e:
                print("Exception: ", e, flush=True)
            print("Poooostsssss", self.liked_posts.all())
        else:
            print("Post not in liked posts", flush=True)
            self.liked_posts.add(post)


class Upravnik(models.Model):
    ulaz = models.OneToOneField(
        Ulaz, on_delete=models.CASCADE, related_name="upravnik"
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    vrsta = models.CharField(
        max_length=50,
        choices=VRSTE_UPRAVNIKA, default="Upravnik - domaće lice"
    )
    firma = models.CharField(max_length=150, null=True, blank=True)
    website = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return "Upravnik stambene zajednice " + str(self.ulaz)

    class Meta:
        verbose_name_plural = "Upravnici"


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # is_director = models.BooleanField()
    image = models.ImageField(default='default.jpg', upload_to="profile_pics")
    o_sebi = models.TextField(null=True, blank=True)
    oceni_upravnika = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        null=True,
        blank=True
    )
    prosecna_ocena = models.FloatField(null=True, blank=True)
    broj_ocenjivaca = models.IntegerField(null=True, blank=True)
    is_director = models.BooleanField(default=False)
    radi_za = models.CharField(max_length=100, null=True, blank=True)
    vrsta_upravnika = models.CharField(max_length=100, null=True, blank=True)
    is_organisation = models.BooleanField(default=False)

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
    CITY_CHOICES = [(x.name, x.name) for x in Grad.objects.all()]
    secr = models.IntegerField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    Grad = models.CharField(max_length=50, null=True, choices=CITY_CHOICES)
    Opština = models.CharField(max_length=50, null=True)
    ulaz = models.ForeignKey(Ulaz, on_delete=models.CASCADE)
    Broj_stana = models.IntegerField(null=True)


class TempPapir(models.Model):
    ulaz = models.ForeignKey(Ulaz, on_delete=models.CASCADE, unique=True)
    foto = models.ImageField(
        upload_to='temp_papir_photos', null=True, blank=True
    )
    city = models.CharField(max_length=60, default='Belgrade')
    ulica_i_broj = models.CharField(
        max_length=50, null=True, blank=True, unique=True
    )
    location = PlainLocationField(
        based_fields=['city'],
        zoom=10,
        default='44.79688084502436,20.477120876312256'
    )

    def __str__(self):
        return self.ulaz.Ulica_i_broj


class TempCepovi(models.Model):
    ulaz = models.ForeignKey(Ulaz, on_delete=models.CASCADE, unique=True)
    foto = models.ImageField(
        upload_to='temp_papir_photos',
        null=True,
        blank=True
    )
    city = models.CharField(max_length=60, default='Belgrade')
    location = PlainLocationField(
        based_fields=['city'],
        zoom=10,
        default='44.79688084502436,20.477120876312256'
    )
    cep_box_filled_date = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.ulaz.Ulica_i_broj


class KomentarUpravnika(models.Model):
    upravnik = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="upravnik_ulaza",
        null=True,
        blank=True
    )
    text = models.TextField(null=True, blank=True)
    autor = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="customuser",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name_plural = "Komentari upravnika"
