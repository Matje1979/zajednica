>>> from users.models import Ulaz, CustomUser, Upravnik
>>> import json
>>> id_list = []
    address_list=[]
    dir_name_list=[]
n=0
with open('data.txt', 'r') as f:
    df = json.load(f)
    for i in df:
        if i['address'] not in address_list:
        ##Creating unique username for every upravnik user to respect unique constraint on usernames

            ##Creating an Ulaz object
            grad = Grad.objects.get(name="Beograd")
            opstina = Opština.objects.get(name="Novi Beograd")
            Ulaz.objects.create(Grad=grad, Opština=opstina, Ulica_i_broj=i['address'])
            ##Check if upravnik is professional. If true,
            if i['director_type'] == 'Професионални управник - домаће лице':
                ##check if upravnik is in users (by id/maticni broj). If not, create new user.
                if i['director_id'] not in id_list:
                    dir_username = i['director'] + str(f'{n:05}')
                    CustomUser.objects.create_user(username=dir_username, password="Testing321", email="mejl@usermail.com", Grad="Beograd", Opština="nulta", Ulica_i_broj="nulti", Broj_stana="nulti", upravnik_id=i['director_id'], is_director=True)
                    id_list.append(i['director_id'])
                    try:
                        ulaz=Ulaz.objects.get(Ulica_i_broj=i['address'])
                    except:
                        print (f'Multiple records at {i["address"]}')
                    usser=CustomUser.objects.last()
                    Upravnik.objects.create(user=usser, ulaz=ulaz, vrsta="Profesionalni upravnik - domaće lice", firma=i['director_company'])
                else:
                        ##If upravnik is already in users, just use the existing user with upravnik id for creating the relevant Upravnik object
                    try:
                        ulaz=Ulaz.objects.get(Ulica_i_broj=i['address'])
                    except:
                        print (f'Multiple records at {i["address"]}')

                    usser=CustomUser.objects.get(upravnik_id=i['director_id'])
                    Upravnik.objects.create(user=usser, ulaz=ulaz, vrsta="Profesionalni upravnik - domaće lice", firma=i['director_company'])
            else:
                CustomUser.objects.create_user(username=dir_username, password="Testing321", email="mejl@usermail.com", Grad="Beograd", Opština="nulta", Ulica_i_broj="nulti", Broj_stana="nulti")
                try:
                    ulaz=Ulaz.objects.get(Ulica_i_broj=i['address'])
                except:
                    print (f'Multiple records at {i["address"]}')
                usser=CustomUser.objects.last()
                Upravnik.objects.create(user=usser, ulaz=ulaz)
            address_list.append(i['address'])
            n+=1
        else:
            pass


