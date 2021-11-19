from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import (
    CustomUserRegisterForm,
    UserUpdateForm,
    ProfileUpdateForm,
    OceniUpravnikaForm,
    PapirForm,
    Register1Form,
    Register2Form,
    Register3Form,
    SecretForm
)
from django.views.generic import ListView
from messaging.forms import MessageForUpravnikForm
from django.contrib.auth.decorators import login_required
from .models import (
    CustomUser,
    Upravnik,
    Profile,
    KomentarUpravnika,
    Ulaz,
    Temp,
    Temp2,
    TempPapir,
    Opština
)
# from dal import autocomplete
from home.models import Post
from django.core.paginator import Paginator
import smtplib
from email.message import EmailMessage
from transliterate import translit
import secrets
from django.http import HttpResponse, JsonResponse


def login_success(request):
    if request.user.username == "Papir_Servis":
        return redirect('papir_servis')
    else:
        return redirect('app-home')


def register(request, pk):
    pk = int(pk)
    temp2 = Temp2.objects.get(id=pk)
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        secr_form = SecretForm(request.POST)
        if form.is_valid() and secr_form.is_valid():
            # Need to handle this somehow
            if secr_form.cleaned_data.get('secr') == temp2.secr:
                new_user = form.save(commit=False)
                new_user.Grad = temp2.Grad
                new_user.Opština = temp2.Opština
                new_user.Ulaz = temp2.ulaz
                new_user.email = temp2.email
                new_user.Ulica_i_broj = temp2.ulaz.Ulica_i_broj
                new_user.Broj_stana = temp2.Broj_stana
                new_user.save()
                messages.success(
                    request,
                    '''
                    Your account has been created! You are now able to log in.
                    '''
                )
                return redirect('login')
    else:
        form = CustomUserRegisterForm()
        secr_form = SecretForm()

    context = {'form': form, 'secr_form': secr_form}
    return render(request, 'users/register.html', context)


def register1(request):
    if request.method == 'POST':
        form = Register1Form(request.POST)
        if form.is_valid():
            yourname = form.cleaned_data['name']
            r_num = secrets.randbelow(10000)
            Temp.objects.create(
                secr=r_num, name=yourname,
                email=form.cleaned_data['email']
            )
            EMAIL_ADDRESS = "damircicic@gmail.com"
            password = "jpjpqiomgxbqustb"
            receiver = form.cleaned_data['email']
            msg = EmailMessage()
            msg['Subject'] = "Šifra za registraciju na ZS."
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = receiver
            content = f"""
            Zdravo {form.cleaned_data['name']}!
            Ovo je šifra za nastavak registracije: {str(r_num)}
            """
            msg.set_content(content)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                # smtp.ehlo()
                # smtp.starttls()
                # smtp.ehlo()

                smtp.login(EMAIL_ADDRESS, password)
                # body = form.instance.content
                # msg = f'Subject: {subject}\n\n{body}'
                # smtp.send_message(msg.encode('utf-8'))
                smtp.send_message(msg)
                messages.success(request, 'Proverite svoju email adresu!')
            return redirect('register2', yourname=yourname)
    else:
        form = Register1Form()
    context = {'form': form}
    return render(request, 'users/register1.html', context)


def register2(request, yourname):
    if request.method == 'POST':
        form = Register2Form(request.POST)
        if form.is_valid():
            if Temp.objects.get(secr=form.cleaned_data['šifra']) is not None:
                temp_id = Temp.objects.get(secr=form.cleaned_data['šifra']).id
                return redirect('register3', temp_id=temp_id)
            else:
                messages.danger(
                    request, 'Uneli ste pogrešnu šifru. Pokušajte ponovo!'
                )
                return redirect('register1')

    form = Register2Form()
    context = {'form': form, 'yourname': yourname}
    return render(request, 'users/register2.html', context)


def register3(request, temp_id):
    if request.method == 'POST':
        form = Register3Form(request.POST)
        if form.is_valid():
            secr = secrets.randbelow(10000)
            temp2 = form.save(commit=False)
            print("Temp_id: ", temp_id)
            temp2.name = Temp.objects.get(id=temp_id).name
            temp2.email = Temp.objects.get(id=temp_id).email
            temp2.secr = secr
            temp2.save()
            Temp.objects.get(pk=temp_id).delete()
            # Sending the secret code the users email (mailbox in future)
            # and a link to the registration page.
            yourname = temp2.name
            r_num = secr
            reg_link = (
                'zajednicastanara.pythonanywhere.com/register/'
                + str(temp2.id)
            )

            EMAIL_ADDRESS = "damircicic@gmail.com"
            password = "jpjpqiomgxbqustb"
            receiver = temp2.email
            msg = EmailMessage()
            msg['Subject'] = "Šifra za registraciju na ZS."
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = receiver
            content = f'''Zdravo {temp2.name}!
                Ovo je šifra za nastavak registracije: {str(r_num)}.
                Ovo je link strane za registraciju: {reg_link}.'''
            msg.set_content(content)

            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                # smtp.ehlo()
                # smtp.starttls()
                # smtp.ehlo()
                smtp.login(EMAIL_ADDRESS, password)
            # body = form.instance.content
            # msg = f'Subject: {subject}\n\n{body}'
            # smtp.send_message(msg.encode('utf-8'))
                smtp.send_message(msg)
                messages.success(
                    request, '''
                    Na vašu adresu će stići
                    pismo sa uputstvima za dalju prijavu.'''
                )
            return redirect('register4', yourname=yourname)

    form = Register3Form()
    context = {'form': form}
    return render(request, 'users/register3.html', context)


def register4(request, yourname):
    context = {'yourname': yourname}
    return render(request, 'users/register4.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES,
            instance=request.user.profile
        )
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    page_title = "Moj profil"

    if request.user.is_director is False:
        ulaz = translit(request.user.Ulaz.Ulica_i_broj, 'sr', reversed=True)
        context = {
            'page_title': page_title,
            'u_form': u_form,
            'p_form': p_form,
            'ulaz': ulaz
        }
    else:
        context = {'page_title': page_title,
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


def user_profile(request, pk):
    user = CustomUser.objects.get(id=pk)
    context = {'user': user}
    return render(request, 'users/user_profile.html', context)


@login_required
def manager_profile(request):
    page_title="Upravnik zgrade"
    upravnik = Upravnik.objects.get(
        ulaz=request.user.Ulaz
    )  # identifikacija defin. deskripcije upravnik
    ulaz = translit(request.user.Ulaz.Ulica_i_broj, 'sr', reversed=True)
    upravnik_set = Upravnik.objects.filter(
        user__username=upravnik.user
    )  # prikupljanje seta def. deskripcija upravnik preko
    posts = Post.objects.filter(author=upravnik.user)
    paginator = Paginator(posts, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # imena upravnika trenutnog ulaza
    total = 0
    n = 0
    for upravnik in upravnik_set:  # za svakog upravnika-deskripciju
        for stanar in CustomUser.objects.filter(Ulaz=upravnik.ulaz):   # za svakog korisnika koji stanuje u ulazu kojim upravlja dati upravnik
            if stanar.username != upravnik.user.username and stanar.profile.oceni_upravnika is not None:   # ako korisnik nije taj upravnik
                total += stanar.profile.oceni_upravnika                                                  # i ako je ocenio upravnika
                n += 1
    if n > 0:                                                                                          # uvećaj total za ocenu upravnika i za 1 ukup. br ocena
        ocena_upravnika = round(float(total/n), 3)  # srednja ocena
        broj_ocenjivaca = n
    else:
        ocena_upravnika = "Nije ocenjivan"
        broj_ocenjivaca = n

    if request.method == 'POST':
        if 'survey-button' in request.POST:
            upravnik_form = OceniUpravnikaForm(request.POST, instance=request.user.profile)
            if upravnik_form.is_valid():
                upravnik_form.save()
                total = 0
                n = 0
                for upravnik in upravnik_set:  # za svakog upravnika-deskripciju
                    for stanar in CustomUser.objects.filter(Ulaz=upravnik.ulaz):   # za svakog korisnika koji stanuje u ulazu kojim upravlja dati upravnik
                        if stanar.username != upravnik.user.username and stanar.profile.oceni_upravnika is not None:   # ako korisnik nije taj upravnik
                            total += stanar.profile.oceni_upravnika                                                  # i ako je ocenio upravnika
                            n += 1
                if n > 0:                                                                                 # uvećaj total za ocenu upravnika i za 1 ukup. br ocena
                    ocena_upravnika = float(total/n)
                else:
                    ocena_upravnika = "Nije ocenjivan"
                if ocena_upravnika != "Nije ocenjivan":
                    upravnik.user.profile.broj_ocenjivaca = n
                    upravnik.user.profile.prosecna_ocena = ocena_upravnika
                    upravnik.user.profile.save()

                messages.success(request, 'Uspešno ste ocenili upravnika!')
                context= {
                    'broj_ocenjivaca': n,
                    'upravnik': upravnik,
                    'ulaz': ulaz,
                    'upravnik_form': upravnik_form,
                    'ocena_upravnika': ocena_upravnika,
                    'page_obj': page_obj,
                    'page_title': page_title
                }
                return render(request, 'users/manager.html', context)
        elif 'message-button' in request.POST:
            message_form = MessageForUpravnikForm(request.POST)
            if message_form.is_valid():
                new_message = message_form.save(commit=False)
                new_message.receiver = upravnik.user
                new_message.sender = request.user
                new_message.save()
                messages.success(request, 'Poslali ste poruku upravniku!')

            upravnik_form = OceniUpravnikaForm(instance=request.user.profile)
            message_form = MessageForUpravnikForm()
            context = {
                'upravnik': upravnik,
                'ulaz': ulaz,
                'upravnik_form': upravnik_form,
                'ocena_upravnika': ocena_upravnika,
                'posts': posts,
                'message_form': message_form,
                'page_title': page_title
            }
            return render(request, 'users/manager.html', context)
    else:
        upravnik_form = OceniUpravnikaForm(instance=request.user.profile)
        message_form = MessageForUpravnikForm()
        # user = request.user
        context = {
            'broj_ocenjivaca': broj_ocenjivaca,
            'upravnik': upravnik,
            'ulaz': ulaz,
            'upravnik_form': upravnik_form,
            'ocena_upravnika': ocena_upravnika,
            'posts': posts,
            'message_form': message_form,
            'page_title': page_title
        }
        return render(request, 'users/manager.html', context)


class ManagersRankingView(ListView):
    """Shows list of grades for managers.
    TO DO: use annotate instead of dict.
    """
    template_name = "users/managers_page.html"
    context_object_name = "upravnici"
    paginate_by = 10

    def get_queryset(self):
        upravnici = (
            Profile.objects.filter(is_director=True)
            .select_related('user')
            # .select_related('user')
            # .select_related('user')
            # .select_related('user')
            # .select_related('user')
            # .select_related('broj_ocenjivaca')
        ).order_by('-prosecna_ocena')[:15]
        return upravnici

    # upravnik_list = []
    # for upravnik in upravnici:
    #     upravnik_dict = dict()
    #     upravnik_dict['username'] = translit(upravnik.user.username, 'sr', reversed=True)
    #     upravnik_dict['id'] = upravnik.user.id
    #     upravnik_dict['ocena'] = upravnik.prosecna_ocena
    #     upravnik_dict['first_name'] = translit(upravnik.user.first_name, 'sr', reversed=True)
    #     upravnik_dict['last_name'] = translit(upravnik.user.last_name, 'sr', reversed=True)
    #     upravnik_dict['broj_ocenjivaca'] = upravnik.broj_ocenjivaca

        # upravnik_list.append(upravnik_dict)
    # print ("U: ", upravnik_list, flush=True)

    # context = {'upravnici': upravnici}
    # return render(request, 'users/managers_page.html', context)


def documents(request):
    page_title = 'Opšti dokumenti'
    if request.user.is_authenticated    :
        ulaz = translit(request.user.Ulaz.Ulica_i_broj, 'sr', reversed=True)
        context = {'ulaz': ulaz, 'page_title': page_title}
        return render(request, 'users/documents.html', context)
    else:
        return render(request, 'users/documents.html')


def manager_public(request, pk):
    upravnik = CustomUser.objects.get(id=pk)
    komentari = KomentarUpravnika.objects.filter(
        upravnik__username=upravnik.username
    )

    # print ("&&&&", upravnik.username)
    context = {'upravnik': upravnik, 'komentari': komentari}

    return render(request, 'users/manager_public_page.html', context)


def papir_servis(request):
    if request.user.username == 'Papir_Servis':
        if request.method == 'POST':
            form = PapirForm(request.POST)
            if form.is_valid():
                a = form.cleaned_data['ulaz']
                form.save()
                a.papir_box_full = False
                a.save()
                messages.success(request, 'Prodaja papira zabeležena!')
                form = PapirForm()
                context = {'form':form}
                return render(request, 'users/papir_servis.html', context)
        else:
            form = PapirForm()

        context = {'form':form}
        return render(request, 'users/papir_servis.html', context)
    else:
        return HttpResponse("<h2>Nemate pristup ovoj stranici</h2>")


def papir_mapa(request):
    filled_boxes = Ulaz.objects.filter(papir_box_full=True)
    # locations = []
    # for box in filled_boxes:
    #     g = geocoder.osm(box.ulaz.Ulica_i_broj + ", " + "Beograd RS")
    #     location = g.latlng
    #     print(location)
    context = {'filled_boxes': filled_boxes}
    return render(request, 'users/papir_mapa.html', context)

def prijavljen_papir(request):
    if request.method == "POST":
        if request.POST['box-status'] == "accept":
            ulaz = Ulaz.objects.get(Ulica_i_broj=request.POST['box-ulaz-address'])
            ulaz.papir_box_full = True
            ulaz.save()
            TempPapir.objects.get(ulaz=ulaz).delete()
            filled_boxes = TempPapir.objects.all()
            if not filled_boxes:
                return redirect('papir_mapa')
        else:
            print ("Box rejected")
            ulaz = Ulaz.objects.get(Ulica_i_broj=request.POST['box-ulaz-address'])
            TempPapir.objects.get(ulaz=ulaz).delete()
            if not filled_boxes:
                context = {'filled_boxes': filled_boxes}
                return redirect('papir_mapa')

        filled_boxes = TempPapir.objects.all()
        context = {'filled_boxes': filled_boxes}
        return render(request, 'users/prijavljen_papir.html', context)
    else:
        filled_boxes = TempPapir.objects.all()
        context={'filled_boxes': filled_boxes}
        return render(request, 'users/prijavljen_papir.html', context)

#AJAX
def load_opstine(request):
    grad_name = request.GET.get("grad_name")
    opstine = Opština.objects.filter(Grad__name=grad_name)
    # print (opstine, flush=True)
    context={"opstine": opstine}
    return render(request, "users/opstine_dropdown_list.html", context)

#AJAX
def load_ulazi(request):
    opstina_id = request.GET.get("opstina_id")
    ulazi = Ulaz.objects.filter(Opština__id=opstina_id)
    # print (ulazi, flush=True)
    context = {"ulazi": ulazi}
    return render(request, "users/ulazi_dropdown_list.html", context)

#AJAX cep_za_hendikep API
def cep_load_opstine(request):
    grad_name = request.GET.get("grad_name")
    opstine = Opština.objects.filter(Grad__name=grad_name)
    # print (opstine, flush=True)
    context = {"opstine": opstine}
    return render(request, "users/cep_opstine_dropdown_list.html", context)

#AJAX cep_za_hendikep API
def cep_load_ulazi(request):
    opstina_name = request.GET.get("opstina_name")
    ulazi = Ulaz.objects.filter(Opština__name=opstina_name)
    ulaz_list = []
    for ulaz in ulazi:
        ulaz_list.append(ulaz.Ulica_i_broj)
    return JsonResponse(ulaz_list, safe=False)
    # print(ulazi, flush=True)
    # context = {"ulazi": ulazi}
    # return render(request, "users/cep_ulazi_dropdown_list.html", context)


