from django.db import models
from django.utils import timezone
from users.models import CustomUser, Ulaz
from django.urls import reverse
from taggit.managers import TaggableManager

# Create your models here.
post_outlines = (
	("Warning", "Warning"),
	("Info", "Info")
)

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	tip = models.CharField(max_length=50, choices=post_outlines, default="Info")
	slug = models.SlugField(max_length=100, null=True)
	tags = TaggableManager()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})
	#This function returns a url of the detail page for the post as a string. View then handles the string. 
	#If you want to redirect to a homepage, for example, in the Create view, you have to set the 'success_url(??)' attribute

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
	kolicina = models.IntegerField(null=True, blank=True)
	ulaz = models.ForeignKey(Ulaz, on_delete=models.CASCADE, null=True, blank=True)
	datum = models.DateTimeField(default=timezone.now)
	cena = models.IntegerField(null=True, blank=True)

