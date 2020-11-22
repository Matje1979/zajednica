from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import (
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment, Papir
from users.models import Upravnik, CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from .forms import CommentForm
import os
import smtplib
from django.template.defaultfilters import slugify
from taggit.models import Tag
from email.message import EmailMessage
from transliterate import translit

# Create your views here.

# posts = [{
#   'author': 'CoreyMs',
#   'title':'Blog Post1 ',
#   'content': 'First post content',
#   'date_posted': 'August 27, 2018'
# },
# {
#   'author': 'Jane Doe',
#   'title':'Blog Post2 ',
#   'content': 'Second post content',
#   'date_posted': 'August 28, 2018'
# }
# ]


def frontpage(request):
    return render(request, "home/frontpage.html")

def home(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, "home/home.html", context)

class PostListView(ListView):
    # model = Post
    template_name = 'home/home.html'
    context_object_name = 'posts'
    paginate_by = 5
    def get_queryset(self):
        posts = Post.objects.filter(author__Ulaz__Ulica_i_broj=self.request.user.Ulaz.Ulica_i_broj).order_by('-date_posted')
        for post in posts:
            for tag in post.tags.all():
                print ("Tag:", tag)
                print ("Tag type:", type(tag))
        return posts
    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context['upravnik'] = Upravnik.objects.get(ulaz=self.request.user.Ulaz)
        context['ulaz'] = translit(self.request.user.Ulaz.Ulica_i_broj, 'sr', reversed=True)
        return context
    # ordering = ['-date_posted']
    #for a ListView, default context object name is object_list, but that can be overriden in the way above.
    #for DetailView, defaul context object name is 'object'

class PostDetailView(DetailView):
    model = Post
    template_name = 'home/post_detail.html'
        
    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['upravnik'] = Upravnik.objects.get(ulaz=self.request.user.Ulaz)
        context['ulaz'] = translit(self.request.user.Ulaz.Ulica_i_broj, 'sr', reversed=True)
        post = get_object_or_404(Post, pk = self.kwargs['pk'])
        context['comments'] = Comment.objects.filter(post=post)
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        c_form = CommentForm(request.POST)
        if c_form.is_valid():    
            obj = c_form.save(commit=False)
            obj.author = self.request.user
            post = get_object_or_404(Post, pk = self.kwargs['pk'])
            obj.post = post
            obj.save()
        return redirect(post)

            #the view sends data by default to a template with the following name pattern: 
    #/app_name/model_name/underscore/type_of_view(list, detail... except for create view, where it expects 'form' instead)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'tip', 'tags']

    def get_context_data(self, **kwargs):
        context = super(PostCreateView, self).get_context_data(**kwargs)
        context['upravnik'] = Upravnik.objects.get(ulaz=self.request.user.Ulaz)
        context['ulaz'] = translit(self.request.user.Ulaz.Ulica_i_broj, 'sr', reversed=True)
        context['common_tags'] = Post.tags.most_common()[:4]
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        neighbors = CustomUser.objects.filter(Ulaz=self.request.user.Ulaz)
        email_list = []
        for neighbor in neighbors:
            email_list.append(neighbor.email)


        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.title)
        newpost.save()
        form.save_m2m()
        EMAIL_ADDRESS = "damircicic@gmail.com"
        password = "jpjpqiomgxbqustb"
        if "upozorenje" in list(form.instance.tags.names()):
            for neighbor in neighbors:
                receiver = neighbor.email
                msg = EmailMessage()
                msg['Subject'] = "Važno obaveštenje"
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = receiver
                # msg['Reply-To'] = "ibnruzd@yahoo.com"
                msg.set_content(form.instance.content)

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    # smtp.ehlo()
                    # smtp.starttls()
                    # smtp.ehlo()

                    smtp.login(EMAIL_ADDRESS, password)

    

                    # body = form.instance.content

                    # msg = f'Subject: {subject}\n\n{body}'

                    # smtp.send_message(msg.encode('utf-8'))
                    smtp.send_message(msg)
        else:
            print (list(form.instance.tags.names()))
        return super().form_valid(form)
    #LoginRequiredMixin serves to block access for users who are not logged in. In addition, it redirects the not logged in user to the login page.
    #On classes we cannot use decorators, instead we use mixins.

def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    #Filter posts by tag name
    posts = Post.objects.filter(tags=tag)
    context = {
    'tag': tag,
    'posts': posts
    }
    return render(request, 'home/home.html', context)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()   #gets the post that we want to update
        if self.request.user == post.author:    #checks if we are the author of the post
            return True
        else:
            return False
    #UserPassesTestMixin serves to block access to update post page to users other than the author of the post
    #How to make a nice notification that access is denied?
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url='/home/'

    def test_func(self):
        post = self.get_object()   #gets the post that we want to update
        if self.request.user == post.author:    #checks if we are the author of the post
            return True
        else:
            return False

def about(request):
    ulaz = translit(request.user.Ulaz.Ulica_i_broj, 'sr', reversed=True)
    context={'ulaz': ulaz}
    return render(request, "home/about.html", context)

def reciklaza(request):
    if request.user.is_authenticated:
        papiri = Papir.objects.filter(ulaz=request.user.Ulaz)
        ulaz = translit(request.user.Ulaz.Ulica_i_broj, 'sr', reversed=True)
        print ("Ulaz", ulaz)
        context = {'papiri': papiri, 'ulaz': ulaz}
        return render(request, 'home/reciklaza.html', context)
    else:
        papiri = Papir.objects.all()
        p_quant = 0
        for papir in papiri: 
            if papir.kolicina != None:
                print ("Kolicina: ", papir.kolicina)
                p_quant += papir.kolicina
        context = {'p_quant': p_quant}
        return render(request, 'home/reciklaza.html', context)


def telefoni(request):
    ulaz = translit(request.user.Ulaz.Ulica_i_broj, 'sr', reversed=True)
    context ={'ulaz': ulaz}
    return render(request, 'home/telefoni.html', context)

def telefoni_p(request):
    return render(request, 'home/telefoni.html')

def upravnik_posts(request, pk):
    ulaz = translit(request.user.Ulaz.Ulica_i_broj, 'sr', reversed=True)
    user = CustomUser.objects.get(id=pk)
    posts = Post.objects.filter(author=user) 
    context ={'posts': posts, 'ulaz': ulaz}
    return render(request, 'home/user_posts.html', context)

