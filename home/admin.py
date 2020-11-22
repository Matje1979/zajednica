from django.contrib import admin
from .models import Post, Papir, Comment, CommentOfComment
from users.forms import PapirForm

class PapirAdmin(admin.ModelAdmin):
    model = Papir
    form = PapirForm

    # class Media:
    #     js = (
    #         'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
    #     )


# Register your models here.


admin.site.register(Post)
admin.site.register(Papir)
admin.site.register(Comment)
admin.site.register(CommentOfComment)
