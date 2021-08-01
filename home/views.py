from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment, Papir, Cepovi
from users.models import (
    Upravnik,
    CustomUser,
    TempPapir,
    Ulaz,
    Profile,
    TempCepovi
)
from messaging.models import MessageForUpravnik
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import CommentForm
import smtplib
from django.template.defaultfilters import slugify
from taggit.models import Tag
from email.message import EmailMessage
from transliterate import translit
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import (
    TempPapirSerializer,
    UlazSerializer,
    PapirPrijavaSerializer,
    PapirSerializer,
    CepoviSerializer,
    TempCepoviSerializer
)
from rest_framework import status
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
    FileUploadParser
)
import json
import time
import re
import base64
from django.core.files.images import ImageFile
# from rest_framework.authentication import (
    # SessionAuthentication,
    # BasicAuthentication
# )

# class CsrfExemptSessionAuthentication(SessionAuthentication):

    # def enforce_csrf(self, request):
    #     return  # To not perform the csrf check previously happening

# This view actually for all users. MessageForUpravnik model despite the name
# is a model for all messages. Name needs to be changed.
# class MessageListView(ListView):
#     template_name = 'home/messages.html'
#     context_object_name = 'usr_messages'
#     paginate_by = 5
#     def get_queryset(self):
#         usr_messages = MessageForUpravnik.objects.filter(receiver=self.request.user)
#         return usr_messages

# # This the same as the previous, just using the DRF.
# class CheckMessagesView(APIView):
#     def get(self, request, pk):
#         print ("Checking messages", flush=True)
#         print ("PK: ", pk, flush=True)
#         messages = MessageForUpravnik.objects.filter(receiver__id=int(pk))
#         serializer = MessageForUpravnikSerializer(messages, many=True)
#         print (messages, flush=True)
#         # result = dict()
#         # result['messages_num'] = len(messages)
#         # result['user_messages'] = messages
#         # print (result, flush=True)
#         return Response(serializer.data)


# Overview of api enpoints.
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Reports of full boxes/': 'papirlist/',
        'List of home managers by grades': 'gradelist/',
        'Full boxes locations': 'p_mapa/',
        'Report collected box': 'p_prijava',

    }
    return Response(api_urls)


# Api for getting the number of collected boxes of lids (cepova) for
# a particular ulaz.
class CepTotal(APIView):
    def get(self, request, address):
        print("Address", address, flush=True)
        ulaz = Ulaz.objects.get(Ulica_i_broj=address)
        res = len(Cepovi.objects.filter(ulaz=ulaz))
        result = {}
        result['tot'] = res
        con = json.dumps(result)
        return Response(con)


# Api for lid collectors. It is getting the list of ulazi with full lid boxes,
# and lets them confirm that they have collected the box
# (and replaced it with an empty one).
class CepConfirmation(APIView):
    def get(self, request):
        """ """
        ulazi = Ulaz.objects.filter(cep_box_full=True)
        serializer = UlazSerializer(ulazi, many=True)
        return Response(serializer.data)

    def post(self, request):
        print("*******************",request.data['address'], flush=True)
        ulaz = Ulaz.objects.get(Ulica_i_broj = request.data['address'])
        Cepovi.objects.create(ulaz=ulaz)
        ulaz.cep_box_full = False
        ulaz.cep_box_filled_date = None
        ulaz.save()
        result = {}
        # result['tot'] = res
        con = json.dumps(result)
        return Response(con)


# Api for info about collected boxes of lids in a particular ulaz.
class CepoviList(APIView):
    def get(self, request, address):
        ulaz = Ulaz.objects.get(Ulica_i_broj=address)
        cepovi = Cepovi.objects.filter(ulaz=ulaz)
        serializer = CepoviSerializer(cepovi, many=True)
        return Response(serializer.data)


# Api for info about collected boxes of paper in a particular ulaz.
class UlazPapirList(APIView):
    def get(self, request, pk):
        ulaz = Ulaz.objects.get(id=pk)
        papiri = Papir.objects.filter(ulaz=ulaz)

        serializer = PapirSerializer(papiri, many=True)
        return Response(serializer.data)


# Api for list of REPORTED full boxes for paper collecting company,
# with options accept and reject.
class TempPapirList(APIView):
    def get(self, request):
        tempp = TempPapir.objects.all()
        serializer = TempPapirSerializer(tempp, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TempPapirSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['box_status'] == 'accept':
                ulaz = Ulaz.objects.get(
                    Ulica_i_broj=serializer.validated_data['box-ulaz-address']
                    )
                ulaz.box_full = True
                ulaz.save()
                print ("Box_full: ", ulaz.papir_box_full)
                TempPapir.objects.get(ulaz=ulaz).delete()
            else:
                ulaz = Ulaz.objects.get(
                    Ulica_i_broj=serializer.validated_data['box-ulaz-address']
                    )
                TempPapir.objects.get(ulaz=ulaz).delete()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Api for list of REPORTED full boxes for paper collecting company,
# with options accept and reject.
class TempCepoviList(APIView):
    def get(self, request):
        tempp = TempCepovi.objects.all()
        serializer = TempCepoviSerializer(tempp, many=True)
        headers = {'Access-Control-Allow-Origin': '*'}
        return Response(serializer.data, headers=headers)

    def post(self, request):
        print ("Payload ********************", request.data, flush=True)
        print(request.data, flush=True)
        if self.request.data['cep_box_status'] == 'accept':
            # draft_request_data = self.request.data.copy()
            # del draft_request_data['cep_box_status']

            # serializer = TempCepoviSerializer(data=draft_request_data)
            # if serializer.is_valid():
            ulaz = Ulaz.objects.get(Ulica_i_broj=self.request.data['address'])
            ulaz.cep_box_full = True
            temp = TempCepovi.objects.get(ulaz=ulaz)
            ulaz.cep_box_filled_date=temp.cep_box_filled_date
            ulaz.save()
            print("Box_full: ", ulaz.cep_box_full)
            TempCepovi.objects.get(ulaz=ulaz).delete()
            tempp = TempCepovi.objects.all()
            serializer = TempCepoviSerializer(tempp, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            ulaz = Ulaz.objects.get(Ulica_i_broj=request.data['address'])
            TempCepovi.objects.get(ulaz=ulaz).delete()
            tempp = TempCepovi.objects.all()
            serializer = TempCepoviSerializer(tempp, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATE)

# Api for map of full boxes of paper
class PapirMapa(APIView):
    def get(self, request):
        filled_boxes = Ulaz.objects.filter(papir_box_full=True)
        serializer = UlazSerializer(filled_boxes, many=True)
        return Response(serializer.data)


# Api for map of full boxes of lids
class CepoviMapa(APIView):
    def get(self, request):
        filled_boxes = Ulaz.objects.filter(cep_box_full=True)
        serializer = UlazSerializer(filled_boxes, many=True)
        return Response(serializer.data)


# Api for reporting that a paper box is full
# @method_decorator(csrf_exempt, name="dispatch")
class PapirPrijava(APIView):
    #Not sure if this plays any role
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    # authentication_classes = (
        # CsrfExemptSessionAuthentication,
        # BasicAuthentication
        # )
    # @csrf_exempt
    def post(self, request, *args, **kwargs):
        # ulaz = Ulaz.objects.get(Ulica_i_broj=request.data['ulaz'])
        #This line is necessary because the field ulaz accepts
        # object ulaz not an address string
        ulaz = Ulaz.objects.get(Ulica_i_broj=request.data['ulaz'])
        if len(TempPapir.objects.filter(ulaz=ulaz)) == 0:
            serializer = PapirPrijavaSerializer(data=request.data)
            #flush=True seems necessary to be able to print
            # in console that is to get server logs in pythonanywhere
            print (serializer, flush=True)
            if serializer.is_valid():
                try:
                    # print (serializer, flush=True)
                    # TempPapir.objects.create(
                    # foto = serializer.validated_data['file'], ulaz = ulaz)

                    # ulaz.box_full = False
                    # ulaz.save()
                    # serializer.save(ulaz=ulaz)
                    #adding external argument ulaz to serializer
                    serializer.save(ulaz=ulaz)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except:
                    raise KeyError()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'Success':'Hvala na prijavi! '}, status=status.HTTP_200_OK)


# Api for reporting that a lid box is full
class CepPrijava(APIView):
    # Not sure if this plays any role
    parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    # authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    # @csrf_exempt
    def post(self, request, *args, **kwargs):
        # ulaz = Ulaz.objects.get(Ulica_i_broj=request.data['ulaz'])
        #This line is necessary because the field ulaz accepts object ulaz not an address string
        ulaz = Ulaz.objects.get(Ulica_i_broj=request.data['ulaz'])
        image_b64 = request.data['imgBase64']
        # print (image_b64, flush=True)

        image_data = re.sub('^data:image/.+;base64,', '', image_b64)
        image_data = base64.b64decode(image_data.encode('ascii'))
        with open("image.png", "wb") as f:
            f.write(image_data)
        # print (image_data, flush=True)
        date = time.time()
        if len(TempCepovi.objects.filter(ulaz=ulaz)) == 0 and ulaz.cep_box_full == False:
            TempCepovi.objects.create(foto = ImageFile(open("image.png", "rb"))  , ulaz = ulaz, cep_box_filled_date=date)
            # serializer = CepPrijavaSerializer(data=request.data)
            # print ("Serializer", serializer, flush=True)
            #flush=True seems necessary to be able to print in console that is to get server logs in pythonanywhere
            # print (serializer, flush=True)
            # if serializer.is_valid():
            #     try:
                    # print (serializer, flush=True)
                    # TempPapir.objects.create(foto = serializer.validated_data['file'], ulaz = ulaz)

                    # ulaz.box_full = False
                    # ulaz.save()
                    # serializer.save(ulaz=ulaz)
                    #adding external argument ulaz to serializer
            #         serializer.save(ulaz=ulaz, cep_box_filled_date=date)
            #         headers = {'Access-Control-Allow-Origin': '*'}
            #         return Response(serializer.data, headers=headers, status=status.HTTP_201_CREATED)
            #     except:
            #         raise KeyError()
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'Success':'Hvala na prijavi! '}, status=status.HTTP_200_OK)
        else:
            return Response({'Success':'Hvala na ponovnoj prijavi! '}, status=status.HTTP_200_OK)


# Api for getting the list of grades of upravniks
class GradesList(APIView):

    def get(self, request):
        grade_list = []
        users_profiles = Profile.objects.filter(is_director = True).order_by('-prosecna_ocena')[:10]
        for profile in users_profiles:
            grade_dict = {}
            grade_dict['name'] = profile.user.first_name + " " + profile.user.last_name
            grade_dict['grade'] = profile.prosecna_ocena
            grade_list.append(grade_dict)
        return Response(grade_list)

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


# This is for the page that users first encounter before registering.
def frontpage(request):
    return render(request, "home/frontpage.html")


# This is for the page that users see when they log in.
@login_required
def home(request):
    if request.user.is_director:
        return redirect('/home_manager')
    else:
        return redirect('/home_user')
    # posts = Post.objects.all()
    # context = {'posts': posts}
    # return render(request, "home/home.html", context)


class PostListView(LoginRequiredMixin, ListView):
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
        context['ulaz'] = self.request.user.Ulaz.Ulica_i_broj
        context['website'] = self.request.user.Ulaz.website
        messages = MessageForUpravnik.objects.filter(receiver=self.request.user)
        print ("user_messages:", messages, flush=True)
        context['user_messages'] = messages
        return context
    # ordering = ['-date_posted']
    #for a ListView, default context object name is object_list, but that can be overriden in the way above.
    #for DetailView, defaul context object name is 'object'


#Base html
def base_layout(request):
	template='home/base.html'
	return render(request,template)


#A View for seeing details about particular posts
class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'home/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['upravnik'] = Upravnik.objects.get(ulaz=self.request.user.Ulaz)
        context['ulaz'] = translit(
            self.request.user.Ulaz.Ulica_i_broj, 'sr', reversed=True
            )
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

            #the view sends data by default to a template with
            # the following name pattern:
            # /app_name/model_name/underscore/type_of_view(
            #list, detail... except for create view, where it expects
            #'form' instead
            # )


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'Sadržaj', 'tip', 'tags']

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
    # LoginRequiredMixin serves to block access for users who are not logged in.
    # In addition, it redirects the not logged in user to the login page.
    # On classes we cannot use decorators, instead we use mixins.


#View for publishing a poll in a post.
class PostCreateView2(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'Sadržaj', 'tip', 'tags', 'anketa_id', 'anketa_title']

    def get_context_data(self, **kwargs):
        context = super(PostCreateView2, self).get_context_data(**kwargs)
        context['upravnik'] = Upravnik.objects.get(ulaz=self.request.user.Ulaz)
        context['ulaz'] = translit(self.request.user.Ulaz.Ulica_i_broj, 'sr', reversed=True)
        context['common_tags'] = Post.tags.most_common()[:4]
        return context

    def get_initial(self):
        return {'anketa_title':self.kwargs['anketa_title'], 'anketa_id': self.kwargs['anketa_id'], 'title': "Anketa"}

    def form_valid(self, form):
        form.instance.author = self.request.user
        # neighbors = CustomUser.objects.filter(Ulaz=self.request.user.Ulaz)
        # email_list = []
        # for neighbor in neighbors:
        #     email_list.append(neighbor.email)


        newpost = form.save(commit=False)
        newpost.slug = slugify(newpost.title)
        newpost.save()
        form.save_m2m()
        # EMAIL_ADDRESS = "damircicic@gmail.com"
        # password = "jpjpqiomgxbqustb"
        # if "upozorenje" in list(form.instance.tags.names()):
        #     for neighbor in neighbors:
        #         receiver = neighbor.email
        #         msg = EmailMessage()
        #         msg['Subject'] = "Važno obaveštenje"
        #         msg['From'] = EMAIL_ADDRESS
        #         msg['To'] = receiver
        #         # msg['Reply-To'] = "ibnruzd@yahoo.com"
        #         msg.set_content(form.instance.content)

        #         with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        #             # smtp.ehlo()
        #             # smtp.starttls()
        #             # smtp.ehlo()

        #             smtp.login(EMAIL_ADDRESS, password)



        #             # body = form.instance.content

        #             # msg = f'Subject: {subject}\n\n{body}'

        #             # smtp.send_message(msg.encode('utf-8'))
        #             smtp.send_message(msg)
        # else:
        #     print (list(form.instance.tags.names()))
        return super().form_valid(form)

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
    fields = ['title', 'Sadržaj']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()   #gets the post that we want to update
        if self.request.user == post.author: # checks if we are the author
            return True
        else:
            return False


# UserPassesTestMixin serves to block access to update
# post page to users other than the author of the post
# How to make a nice notification that access is denied?
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url='/home/'

    def test_func(self):
        post = self.get_object()   #gets the post that we want to update
        if self.request.user == post.author:    #checks if we are the author
            return True
        else:
            return False


def about(request):
    ulaz = translit(request.user.Ulaz.Ulica_i_broj, 'sr', reversed=True)
    context={'ulaz': ulaz}
    return render(request, "home/about.html", context)


# @login_required
def reciklaza(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            papiri = Papir.objects.filter(ulaz=request.user.Ulaz)
            ulaz = translit(request.user.Ulaz.Ulica_i_broj, 'sr', reversed=True)
            print ("Ulaz", ulaz)
            context = {'papiri': papiri, 'ulaz': ulaz}
            return render(request, 'home/reciklaza.html', context)
            # if request.POST.get('vrsta') == "Papir":
            print ("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
            print ("request Post")
            a = request.POST.get('ulaz')
            ulaz = Ulaz.objects.get(Ulica_i_broj=a)
            print ("Ovo je ulaz: ", ulaz)
            print (ulaz.location)
            if not TempPapir.objects.filter(ulaz=ulaz):
                if request.FILES.get('foto'):
                    # <script>
                    #     var loc = ulaz.location;
                    #     console.log(loc)
                    # </script>
                    print (ulaz.location)
                    TempPapir.objects.create(
                        ulaz=ulaz, foto=request.FILES.get('foto'),
                        ulica_i_broj = ulaz.Ulica_i_broj, location = ulaz.location
                        )

                    messages.success(
                        request,
                        "Hvala što ste nas obavestili o popunjenosti kutije!"
                        )
                else:
                    messages.warning(
                        request,
                        "Niste napravili fotografiju, molim vas probajte ponovo."
                        )

            else:

                print (request.FILES.get('foto'))
                if request.FILES.get('foto'):
                    print (request.FILES.get('foto'))
                    messages.warning (
                        request,
                        "Niste napravili fotografiju, molim vas probajte ponovo."
                        )
                else:
                    messages.warning (
                        request,
                        "Niste napravili fotografiju, molim vas probajte ponovo."
                        )
                    print ("photo not taken")


            # print ("Method Post")
            # if request.user.is_authenticated:

            # else:
            #     papiri = Papir.objects.all()
            #     p_quant = 0
            #     for papir in papiri:
            #         if papir.kolicina != None:
            #             print ("Kolicina: ", papir.kolicina)
            #             p_quant += papir.kolicina
            #     context = {'p_quant': p_quant}
            #     return render(request, 'home/reciklaza.html', context)

        else:
            papiri = Papir.objects.filter(ulaz=request.user.Ulaz)
            ulaz = translit(request.user.Ulaz.Ulica_i_broj, 'sr', reversed=True)
            print ("Ulaz", ulaz)
            total_kolicina = 0
            total_cena = 0
            for papir in papiri:
                total_kolicina += papir.kolicina
                total_cena += papir.cena
                print (total_cena)
                print (total_kolicina)

            context = {
                'total_kolicina': total_kolicina,
                'total_cena': total_cena,
                'papiri': papiri, 'ulaz': ulaz
                }
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
    if not request.user.is_director:
        ulaz = translit(request.user.Ulaz.Ulica_i_broj, 'sr', reversed=True)
        context ={'ulaz': ulaz}

    else:
        context = {'ulaz': 'Početna'}

    return render(request, 'home/telefoni.html', context)


def telefoni_p(request):
    return render(request, 'home/telefoni.html')


def upravnik_posts(request, pk):
    ulaz = translit(request.user.Ulaz.Ulica_i_broj, 'sr', reversed=True)
    user = CustomUser.objects.get(id=pk)
    posts = Post.objects.filter(author=user)
    context ={'posts': posts, 'ulaz': ulaz}
    return render(request, 'home/user_posts.html', context)


def home_manager(request):
    msgs_by_ulazi = {}
    ulazi = Ulaz.objects.filter(upravnik__user=request.user)
    for ulaz in ulazi:
        ulaz_msgs_list = []
        ulaz_msgs = MessageForUpravnik.objects.filter(sender__Ulaz = ulaz)
        ulaz_msgs_query = ulaz_msgs.filter(receiver=request.user)
        if len(ulaz_msgs_query) > 0:
            for msg in ulaz_msgs_query:
                ulaz_msgs_list.append(msg)
                msgs_by_ulazi[ulaz] = len(ulaz_msgs_list)
        else:
            msgs_by_ulazi[ulaz] = 0
    print (len(msgs_by_ulazi.items()), flush=True)

    context = {
        'ulaz': 'Početna',
        'ulazi': ulazi,
        'msgs_by_ulazi': msgs_by_ulazi
        }
    return render(request, 'home/director_dashboard.html', context)

# class MngrMessageListView(ListView):
#     # model = Post
#     template_name = 'home/mngr_messages.html'
#     context_object_name = 'msgs'
#     paginate_by = 5
#     def get_queryset(self):
#         print (self.request.user, flush=True)
#         msgs = MessageForUpravnik.objects.filter(receiver=self.request.user)
#         for msg in msgs:
#             msg.seen = True
#             msg.save()
#         print (msgs, flush=True)
#         return msgs
#     # ordering = ['-date_posted']
#     #for a ListView, default context object name is object_list, but that can be overriden in the way above.
#     #for DetailView, defaul context object name is 'object'
# class MsgDetailView(DetailView):
#     model = MessageForUpravnik
#     template_name = 'home/msg_detail.html'

#     def get_context_data(self, **kwargs):
#         context = super(MsgDetailView, self).get_context_data(**kwargs)
#         msg = get_object_or_404(MessageForUpravnik, pk = self.kwargs['pk'])
#         if msg:
#             msg.read = True
#             msg.save()
#         context['msg'] = msg
#         context['form'] = MessageReplyForm()
#         # context['form'] = CommentForm()
#         return context

#     def post(self, request, *args, **kwargs):
#         c_form = MessageReplyForm(request.POST)
#         if c_form.is_valid():
#             obj = c_form.save(commit=False)
#             obj.sender = self.request.user
#             msg = get_object_or_404(MessageForUpravnik, pk = self.kwargs['pk'])
#             receiver = msg.sender
#             obj.receiver = receiver
#             obj.save()
#         return redirect('/manager_messages')


# class MsgDeleteView(LoginRequiredMixin, DeleteView):

#     model = MessageForUpravnik
#     success_url='/manager_messages/'


def malfunction_report(request):
    return render(request, "home/malfunction.html")


    # def test_func(self):
    #     post = self.get_object()   #gets the post that we want to update
    #     if self.request.user == post.author:    #checks if we are the author of the post
    #         return True
    #     else:
    #         return False

    # def post(self, request, *args, **kwargs):
    #     c_form = CommentForm(request.POST)
    #     if c_form.is_valid():
    #         obj = c_form.save(commit=False)
    #         obj.author = self.request.user
    #         post = get_object_or_404(Post, pk = self.kwargs['pk'])
    #         obj.post = post
    #         obj.save()
    #     return redirect(post)

            #the view sends data by default to a template with the following name pattern:
    #/app_name/model_name/underscore/type_of_view(list, detail... except for create view, where it expects 'form' instead)
