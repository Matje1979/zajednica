from django.contrib import admin
from .models import Post, Papir, Comment, CommentOfComment, Cepovi
from users.forms import PapirForm
from users.models import TempCepovi


class PapirAdmin(admin.ModelAdmin):
    model = Papir
    form = PapirForm

    # class Media:
    #     js = (
    #         'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
    #     )


# Register your models here.

# class CepoviAdmin(admin.ModelAdmin):
#     model = Papir
#     form = PapirForm


admin.site.register(Post)
admin.site.register(Papir)
admin.site.register(Comment)
admin.site.register(CommentOfComment)
admin.site.register(Cepovi)
admin.site.register(TempCepovi)
