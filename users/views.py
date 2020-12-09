from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserRegisterForm, UserUpdateForm, ProfileUpdateForm, OceniUpravnikaForm, PapirForm, MessageForUpravnikForm, Register1Form, Register2Form, Register3Form, SecretForm
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Upravnik, Profile, KomentarUpravnika, Ulaz, Temp, Temp2, TempPapir
# from dal import autocomplete
from home.models import Post
from django.core.paginator import Paginator
import smtplib
from email.message import EmailMessage
from transliterate import translit
import secrets
from django.http import HttpResponse
import geocoder


# Create your views here.

def login_success(request):
    if request.user.username == "Papir_Servis":
        return redirect('papir_servis')
    else:
        return redirect('app-home')

def register(request, pk):
    pk = int(pk)
    print ("Pk: ", pk)
    temp2 = Temp2.objects.get(id=pk)
    print ("Name: ", temp2.name)
    if request.method == 'POST':
        form = CustomUserRegisterForm(request.POST)
        secr_form = SecretForm(request.POST)
        if form.is_valid() and secr_form.is_valid():
            ##Need to handle this somehow
            if secr_form.cleaned_data.get('secr') == temp2.secr:
                new_user = form.save(commit=False)        
                new_user.Grad = temp2.Grad        
                new_user.Opština = temp2.Opština      
                new_user.Ulaz = temp2.ulaz      
                new_user.email = temp2.email     
                username = form.cleaned_data.get('username')
                new_user.save()
                messages.success(request, f'Your account has been created! You are now able to log in.')
                return redirect('login')
    else:
        form = CustomUserRegisterForm()
        secr_form = SecretForm()

    context={'form':form, 'secr_form':secr_form}
    return render(request, 'users/register.html', context)

def register1(request):
    if request.method == 'POST':
        form = Register1Form(request.POST)
        if form.is_valid():
            yourname = form.cleaned_data['name']
            r_num = secrets.randbelow(10000)
            Temp.objects.create(secr=r_num, name=yourname, email=form.cleaned_data['email'])
            EMAIL_ADDRESS = "damircicic@gmail.com"
            password = "jpjpqiomgxbqustb"
            receiver = form.cleaned_data['email']
            msg = EmailMessage()
            msg['Subject'] = "Šifra za registraciju na ZS."
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = receiver
            content = f"Zdravo {form.cleaned_data['name']}! Ovo je šifra za nastavak registracije: {str(r_num)}"
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
                messages.success(request, f'Proverite svoju email adresu!')
            return redirect('register2', yourname=yourname)
    else:
        form = Register1Form()
    context = {'form':form}
    return render(request, 'users/register1.html', context)

def register2(request, yourname):
    if request.method == 'POST':
        form = Register2Form(request.POST)
        if form.is_valid():
            if Temp.objects.get(secr=form.cleaned_data['šifra']) != None:
                temp_id = Temp.objects.get(secr=form.cleaned_data['šifra']).id
                return redirect('register3', temp_id=temp_id )
            else:
                messages.danger(request, f'Uneli ste pogrešnu šifru. Pokušajte ponovo!')
                return redirect('register1')

    form = Register2Form()
    context = {'form':form, 'yourname': yourname}
    return render(request, 'users/register2.html', context)

def register3(request, temp_id):
    if request.method == 'POST':
        form = Register3Form(request.POST)
        if form.is_valid():
            secr = secrets.randbelow(10000)
            temp2 = form.save(commit=False)
            print ("Temp_id: ", temp_id)
            temp2.name = Temp.objects.get(id=temp_id).name
            temp2.email = Temp.objects.get(id=temp_id).email
            temp2.secr = secr
            temp2.save()
            Temp.objects.get(pk=temp_id).delete()
            ##Sending the secret code the users email (mailbox in future) and a link to the registration page
            yourname = temp2.name
            r_num = secr
            reg_link = 'localhost:8000/register/' + str(temp2.id)

            EMAIL_ADDRESS = "damircicic@gmail.com"
            password = "jpjpqiomgxbqustb"
            receiver = temp2.email
            msg = EmailMessage()
            msg['Subject'] = "Šifra za registraciju na ZS."
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = receiver
            content = f"Zdravo {temp2.name}! Ovo je šifra za nastavak registracije: {str(r_num)}. Ovo je link strane za registraciju: {reg_link}."
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
                messages.success(request, f'Na vašu adresu će stići pismo sa uputstvima za dalju prijavu.')
            return redirect('register4', yourname=yourname)

    form = Register3Form()
    context = {'form':form}
    return render(request, 'users/register3.html', context)

def register4(request, yourname):
    context = {'yourname':yourname}
    return render(request, 'users/register4.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    ulaz = translit(request.user.Ulaz.Ulica_i_broj, 'sr', reversed=True)
        
    context = {'u_form': u_form, 'p_form': p_form, 'ulaz': ulaz}
    return render(request, 'users/profile.html', context)

def user_profile(request, pk):
    user = CustomUser.objects.get(id = pk)
    context = {'user': user}
    return render(request, 'users/user_profile.html', context)

def manager_profile(request):
    upravnik = Upravnik.objects.get(ulaz=request.user.Ulaz) #identifikacija defin. deskripcije upravnik
    ulaz = translit(request.user.Ulaz.Ulica_i_broj, 'sr', reversed=True)
    upravnik_set = Upravnik.objects.filter(user__username=upravnik.user) #prikupljanje seta def. deskripcija upravnik preko
    posts = Post.objects.filter(author=upravnik.user) 
    paginator = Paginator(posts, 5) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
                                                        #imena upravnika trenutnog ulaza
    total = 0  
    n = 0                                                                
    for upravnik in upravnik_set:  #za svakog upravnika-deskripciju
        for stanar in CustomUser.objects.filter(Ulaz=upravnik.ulaz):   #za svakog korisnika koji stanuje u ulazu kojim upravlja dati upravnik      
            if stanar.username != upravnik.user.username and stanar.profile.oceni_upravnika != None:   #ako korisnik nije taj upravnik 
                total+=stanar.profile.oceni_upravnika                                                  #i ako je ocenio upravnika
                n+=1
    if n > 0:                                                                                    #uvećaj total za ocenu upravnika i za 1 ukup. br ocena
        ocena_upravnika = float(total/n)  #srednja ocena
    else:
        ocena_upravnika = "Nije ocenjivan"

    if request.method == 'POST':
        if 'survey-button' in request.POST:
            upravnik_form = OceniUpravnikaForm(request.POST, instance=request.user.profile)
            if upravnik_form.is_valid():
                upravnik_form.save()
                total = 0  
                n = 0                                                                
                for upravnik in upravnik_set:  #za svakog upravnika-deskripciju
                    for stanar in CustomUser.objects.filter(Ulaz=upravnik.ulaz):   #za svakog korisnika koji stanuje u ulazu kojim upravlja dati upravnik      
                        if stanar.username != upravnik.user.username and stanar.profile.oceni_upravnika != None:   #ako korisnik nije taj upravnik 
                            total+=stanar.profile.oceni_upravnika                                                  #i ako je ocenio upravnika
                            n+=1  
                if n > 0:                                                                                 #uvećaj total za ocenu upravnika i za 1 ukup. br ocena
                    ocena_upravnika = float(total/n) 
                else:
                    ocena_upravnika = "Nije ocenjivan"
                if ocena_upravnika != "Nije ocenjivan":
                    upravnik.user.profile.prosecna_ocena = ocena_upravnika
                    upravnik.user.profile.save()

                messages.success(request, f'Uspešno ste ocenili upravnika!')
                context= {'upravnik': upravnik, 'ulaz': ulaz, 'upravnik_form': upravnik_form, 'ocena_upravnika': ocena_upravnika, 'page_obj':page_obj}
                return render(request, 'users/manager.html', context)
        elif 'message-button' in request.POST:
            message_form = MessageForUpravnikForm(request.POST)
            if message_form.is_valid():
                EMAIL_ADDRESS = "damircicic@gmail.com"
                password = "jpjpqiomgxbqustb"
                receiver = "damircicic@gmail.com"
                msg = EmailMessage()
                msg['Subject'] = message_form.cleaned_data['title']
                msg['From'] = EMAIL_ADDRESS
                msg['To'] = receiver
                msg['Reply-To'] = "ibnruzd@yahoo.com"
                content = message_form.cleaned_data['content']
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
                    messages.success(request, f'Poslali ste poruku upravniku!')
            upravnik_form = OceniUpravnikaForm(instance=request.user.profile)
            message_form = MessageForUpravnikForm()
            context= {'upravnik': upravnik, 'ulaz': ulaz, 'upravnik_form': upravnik_form, 'ocena_upravnika': ocena_upravnika, 'posts':posts, 'message_form': message_form}
            return render(request, 'users/manager.html', context)
    else:
        
        upravnik_form = OceniUpravnikaForm(instance=request.user.profile)
        message_form = MessageForUpravnikForm()
        print (upravnik)
        # user = request.user
        context= {'upravnik': upravnik, 'ulaz': ulaz, 'upravnik_form': upravnik_form, 'ocena_upravnika': ocena_upravnika, 'posts':posts, 'message_form': message_form}
        return render(request, 'users/manager.html', context)

def managers_page(request):
    # ulaz = request.user.Ulaz.Ulica_i_broj
    upravnici = Profile.objects.filter(is_director = True).order_by('-prosecna_ocena')[:100]
    upravnik_list = []
    for upravnik in upravnici:
        upravnik_dict = dict()
        upravnik_dict['username'] = upravnik.user.username
        upravnik_dict['id'] = upravnik.user.id
        upravnik_dict['ocena'] = upravnik.prosecna_ocena
        upravnik_dict['first_name'] = upravnik.user.first_name
        upravnik_dict['last_name'] = upravnik.user.last_name
        upravnik_list.append(upravnik_dict)
    print (upravnik_list)

    context = {'upravnik_list': upravnik_list}
    return render(request, 'users/managers_page.html', context)

def documents(request):
    if request.user.is_authenticated    :
        ulaz = translit(request.user.Ulaz.Ulica_i_broj, 'sr', reversed=True)
        context = {'ulaz': ulaz}
        return render(request, 'users/documents.html', context)
    else:
        return render(request, 'users/documents.html')


def manager_public(request, pk):
    upravnik = CustomUser.objects.get(id=pk)
    komentari=KomentarUpravnika.objects.filter(upravnik__username=upravnik.username)

    # print ("&&&&", upravnik.username)
    context = {'upravnik':upravnik, 'komentari': komentari}

    return render(request, 'users/manager_public_page.html', context)

# class UlazAutocomplete(autocomplete.Select2QuerySetView):
#     def get_queryset(self):
#         if not self.request.user.is_authenticated:
#             # print ('User not authenticated')
#             return Ulaz.objects.none()

#         qs = Ulaz.objects.all()
#         # print ("This is qs")
#         # print ("This is q: ", self.q)
#         if self.q:
#             qs = qs.filter(Ulica_i_broj__istartswith=self.q)

#             # print ('This is q: ', self.q)
#         print ('This is qs: ', qs)

#         return qs

def papir_servis(request):
    if request.user.username == 'Papir_Servis':
        if request.method == 'POST':
            form = PapirForm(request.POST)
            if form.is_valid():
                a = form.cleaned_data['ulaz']
                form.save()
                a.box_full = False
                a.save()
                messages.success(request, f'Prodaja papira zabeležena!')
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
    filled_boxes = Ulaz.objects.filter(box_full=True)
    # locations = []
    # for box in filled_boxes:
    #     g = geocoder.osm(box.ulaz.Ulica_i_broj + ", " + "Beograd RS")
    #     location = g.latlng
    #     print (location)
    context = {'filled_boxes': filled_boxes}
    return render(request, 'users/papir_mapa.html', context)

def prijavljen_papir(request):
    if request.method == "POST":
        print ("POST")
        if request.POST['box-status'] == "accept":
            print ("Box acccepted")
            ulaz = Ulaz.objects.get(Ulica_i_broj=request.POST['box-ulaz-address'])
            ulaz.box_full = True
            ulaz.save()
            print ("Box_full: ", ulaz.box_full)
            TempPapir.objects.get(ulaz=ulaz).delete()
        else:
            print ("Box rejected")
            ulaz = Ulaz.objects.get(Ulica_i_broj=request.POST['box-ulaz-address'])
            TempPapir.objects.get(ulaz=ulaz).delete()

        filled_boxes = TempPapir.objects.all()
        context={'filled_boxes':filled_boxes}
        return render(request, 'users/prijavljen_papir.html', context)
    else:
        filled_boxes = TempPapir.objects.all()
        context={'filled_boxes':filled_boxes}
        return render(request, 'users/prijavljen_papir.html', context)



# def prijava(request):
#     url = request.path
#     if 'en' in url:
#         url = url[3:]
#     else:
#         url = url
        
#     cpi = Profil.objects.first()
        
#     baneri = Baner.objects.all().order_by('-Datum_objave')
#     baner_list = []
#     if len(baneri) <= 5:
#         for baner in baneri:
#             baner_list.append(baner)
#     else:
#         baner_list = baneri[:5]
        
#     if request.method == 'POST':
#         name = request.POST['ime']
#         surname = request.POST['prezime']
#         email = request.POST['email']
#         tura = request.POST['vodjenja']
#         random_num = secrets.randbelow(1000000)
        
#         print (name)
#         print (surname)
        
#         num=str(random_num)
        
#         a = TempPrijava(Ime = name, Prezime = surname, Email = email, Tura = tura, random_num = random_num)
#         a.save()
        
#         msg = MIMEMultipart("alternative")
#         msg["Subject"] = "reservation test"
#         msg["From"] = "reservations@cpi.rs"
#         msg["To"] = email
        

#         port = 465

#         password = 'jpjpqiomgxbqustb'


#         context = ssl.create_default_context()
        
#         message = f"""\  
#         Pozdrav,
#         Potvrdite prijavu za vodjenje klikom na ovaj link: https://www.cpi.rs/potvrda/{num}
        
#         """
        
#         html = f"""\  
#         <html>
#             <body>
#                 <p>Pozdrav,<br>
#                 potvrdite prijavu za vodjenje klikom na ovaj link: <a href="https://www.cpi.rs/potvrda/{num}">link</a>
#                 </p>
#             </body>
#         </html>
        
#         """
        
#         part1 = MIMEText(message, "plain")
#         part2 = MIMEText(html, "html")
        
#         msg.attach(part1)
#         msg.attach(part2)

        
#         with smtplib.SMTP_SSL("mail.cpi.rs", port, context = context) as server:
#                 server.login("reservations@cpi.rs", password)
#                 server.sendmail("reservations@cpi.rs", email, msg.as_string()) 
        
#         return render(request, 'cpi/potvrda_prijave.html')
#     else:
#         return HttpResponseNotFound('<h1>Page not found</h1>')
        
# def potvrda(request, rand_num):
#     try:
#         # rand_num = int(rand_num)
#         a = TempPrijava.objects.get(random_num = rand_num)
#         ime = a.Ime
#         prezime = a.Prezime
#         email = a.Email
#         tura = a.Tura
        
#         print (tura)
#         print (ime)

#         b = Prijava.objects.create(Ime = ime, Prezime = prezime, Email = email, Tura = tura)

#         a.delete()
        
#     except Exception as e:
#         print (e)

#     return render(request, 'cpi/success.html')   