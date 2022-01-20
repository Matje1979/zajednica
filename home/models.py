from django.db import models
from django.utils import timezone
from users.models import CustomUser, Ulaz
from django.urls import reverse
from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
post_outlines = (("Warning", "Warning"), ("Info", "Info"))


class Post(models.Model):
    title = models.CharField("Naslov", max_length=100)
    Sadržaj = RichTextUploadingField(null=True, blank=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tip = models.CharField(
        max_length=50, choices=post_outlines, default="Info"
    )
    slug = models.SlugField(max_length=100, null=True)
    tags = TaggableManager("Tagovi")
    anketa_id = models.IntegerField(blank=True, null=True)
    anketa_title = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("app-home")


    # 	return reverse('app-home', kwargs={'pk': self.pk})
    # This function returns a url of the detail page for the post as a string.
    # View then handles the string.
    # If you want to redirect to a homepage, for example, in the Create view,
    # you have to set the 'success_url(??)' attribute.


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    text = models.TextField(null=True)


class CommentOfComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)
    text = models.TextField(null=True)


class Papir(models.Model):
    kolicina = models.IntegerField(
        validators=[MinValueValidator(1)], null=True, blank=True
    )
    ulaz = models.ForeignKey(
        Ulaz, on_delete=models.CASCADE, null=True, blank=True
    )
    datum = models.DateTimeField(default=timezone.now)
    cena = models.IntegerField(
        validators=[MinValueValidator(1)], null=True, blank=True
    )

    def __str__(self):
        return self.datum

    class Meta:
        verbose_name_plural = "Papiri"


class Cepovi(models.Model):
    ulaz = models.ForeignKey(
        Ulaz, on_delete=models.CASCADE, null=True, blank=True
    )
    datum = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.datum)

    class Meta:
        verbose_name_plural = "Čepovi"

