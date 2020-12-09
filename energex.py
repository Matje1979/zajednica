from bs4 import BeautifulSoup
import requests
from urllib import request
from transliterate import translit
import string
import csv
import re
import django
from django.conf import settings
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "home_manager.settings")

django.setup()
from users.models import Ulaz



# print ("Soup")

# source = requests.get('https://www.epsdistribucija.rs/index.php/planirana-iskljucenja/planirana-bgd').text
def energyCuts(location):

    print ("Searching cuts")

    with request.urlopen('https://www.epsdistribucija.rs/Dan_1_Iskljucenja.htm') as response:
       html = response.read()
       # print (html)

    # print (source)


    soup = BeautifulSoup(html, 'lxml')

    text = location

    text = translit(text, 'sr')

    final_list = {}

    # print (soup.prettify())
    ##Finding the column element with specified text
    county = soup.find_all('td', text=text)
    for item in county:
        # print (item)
    ##Finding the parent of that element
        row = item.find_parent('tr')

        # print (row.prettify())
        # print ()
        # print ()
        ##printing (the text of) the third child of this element (as a list)
        address_list = row.select('tr > td')[2].get_text(strip=True).split(', ')
        # print (address_list)



        x = address_list[0].split(':')
        # print (x)

        if 'Насеље' in x[0]:

        # print (x[1:])


            c = x[1:]
            c[0] = c[0].strip()
            l = ':'.join(c)
            # print (l)
            k = []
            k.append(l)
            m = k + address_list[1:]
        else: 
            m = address_list

        # print (d)
        # address_list = row.select('tr > td')[2].get_text(strip=True).split(', ')

        # print (address_list)
        # test_string = '33A'\
        alphabet = ['A', 'B', 'C', 'Č', 'Ć', 'D', 'Dž', 'Đ', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'Lj', 'M', 'N', 'Nj', 'O', 'P', 'R', 'S', 'Š', 'T', 'U', 'V', 'Z', 'Ž']
        # print ('Alphabet:', alphabet)

        # print (alphabet.index(B))


        # test_string = ''.join((filter(lambda i: i not in alphabet, test_string)))

        # print (test_string)

        
            
        for address in m:
            new_list = address.split(':')
            # print (new_list)
            ulica = new_list[0]
            ulica = ulica.strip()
            brojevi = new_list[1]
            brojevi = brojevi.split(',')

            new_brojevi = []
            for broj in brojevi:
                #eliminacija praznog prostora u nizu.
                if broj == '':
                    pass
                else:
                    new_broj = broj.replace(' ', '')
                    new_brojevi.append(new_broj)
                    # print (new_brojevi)
                    # final_list.append([ulica, new_broj])
            # print(final_list)
            for broj in new_brojevi:
                print ('Broj: ',broj)
                print ()
                if '-' in broj:
                    niz_brojeva = broj.split('-')
                    if '/' in niz_brojeva[0]:
                        pocetni = niz_brojeva[0][:niz_brojeva[0].index('/')]
                        for i in range(int(niz_brojeva[0][niz_brojeva[0].index('/'):]), 20):
                            final_list[ulica + " " + niz_brojeva[0][:niz_brojeva[1].index('/') + 1]+ str(i)] = ulica + " " + niz_brojeva[0][:niz_brojeva[1].index('/') + 1]+ str(i)
                        print ("********pocetni", pocetni)
                    else:
                        pocetni = niz_brojeva[0]
                    if '/' in niz_brojeva[1]:
                        poslednji = niz_brojeva[1][:niz_brojeva[1].index('/')]
                        for i in range(1, int(niz_brojeva[1][niz_brojeva[1].index('/') + 1:]) + 1):
                            final_list[ulica + " " + niz_brojeva[1][:niz_brojeva[1].index('/') + 1]+ str(i)] = ulica + " " + niz_brojeva[1][:niz_brojeva[1].index('/') + 1]+ str(i)
                        print("************poslednji", poslednji)
                    else:
                        poslednji = niz_brojeva[1]
                    poc_num = re.sub("[A-Za-z]+", "", pocetni)
                    pos_num = re.sub("[A-Za-z]+", "", poslednji)
                    # print (poc_num)
                    # print (pos_num)
                    # print ()
                    if poc_num == pos_num:

                        #eliminacija svega sto je alfabet

                        # num = ''.join(filter(lambda i: i not in alphabet, pocetni))
                        if pocetni == poc_num:
                            pocetno_slovo = "A"
                        else:
                            for i in pocetni:
                                if i not in poc_num:
                                    pocetno_slovo = i
                        if poslednji == pos_num:
                            poslednje_slovo = "Z"
                        else:    
                            for i in poslednji:
                                if i not in poc_num:
                                    poslednje_slovo = i
                        poslednje_slovo_index = alphabet.index(poslednje_slovo)
                        pocetno_slovo_index = alphabet.index(pocetno_slovo)
            #           #niz slova izmedju pocetnog i zavrsnog slova
                        list_of_chars = alphabet[pocetno_slovo_index + 1: poslednje_slovo_index]
            #           #formiranje brojeva koji su izmedju potencijalno
                        for char in list_of_chars:
                            broj_ulaza = poc_num + char
                            final_list[ulica + " " + broj_ulaza] = ulica + " " + broj_ulaza
            #               #sada se proverava da li je taj broj ulaza postojeci broj uporedjivanjem sa ulazima u bazi. 
            #               #Ako jeste, kreira se iskljucenje objekat.
                        # print (final_list)
                    else:

            #           #Treba proveriti da li je u pocetnom ili poslednjem slovo
                        if not pocetni.isdigit():
                            print ("Pocetni not a digit")
                            pocetni_list = []
                            # print ('Alph:', alphabet)
                            # print ('Poc:', pocetni)
                            for i in pocetni:
                                # print ('I: ', i)
                                if i.isdigit():
                                # if i != 'A':
                                    # print ('A != ', i)
                                    pocetni_list.append(i)
                            # print ('Pocetni_list: ', pocetni_list)
                            pocetni_num = ''.join(pocetni_list)
                            print ('Pocetni_num& ', pocetni_num)
                            # print (pocetni_num)
         #                    #Ako jeste, upotrebiti gornju metodu da se selektirajum potencijalni brojevi ulaza.Ako nije dodati samo taj broj u listu.
                            # num = ''.join(filter(lambda i: i not in alphabet, pocetni_list))
                            # print ('Pocetni: ', pocetni)
                            # print ('Num: ', num)
                            for i in pocetni:
                                # print (i)
                                if i not in pocetni_num:
                                    pocetno_slovo = i
                                    # print (pocetno_slovo)
                            pocetno_slovo = translit(pocetno_slovo, 'sr', reversed=True)
                            pocetno_slovo_index = alphabet.index(pocetno_slovo)
                            list_of_chars = alphabet[pocetno_slovo_index + 1:]
                            final_list[ulica + " " + pocetni] = ulica + " " + pocetni
                #           #formiranje brojeva koji su izmedju potencijalno
                            for char in list_of_chars:
                                broj_ulaza = pocetni_num + char                        
                                final_list[ulica + " " + broj_ulaza] = ulica + " " + broj_ulaza
                        else:
                            final_list[ulica + " " + pocetni] = ulica + " " + pocetni
                            pocetni_num = pocetni
                        print ('pocetni_num: ', pocetni_num)
                        
                        poslednji_lower = poslednji.lower()
                        pocetni_lower = pocetni.lower()
                        if not poslednji.isdigit():
                            poslednji_list = []
                            # print ('Alph:', alphabet)
                            # print ('Poc:', pocetni)
                            for i in poslednji:
                                # print ('I: ', i)
                                if i.isdigit():
                                # if i != 'A':
                                    # print ('A != ', i)
                                    poslednji_list.append(i)
                            # print ('Pocetni_list: ', pocetni_list)
                            poslednji_num = ''.join(poslednji_list)
                            print ("Poslednji not a digit")
                            # poslednji_num = ''.join((filter(lambda i: i not in alphabet, pocetni)))
                            print ("poslednji_num& ", poslednji_num)
                            for i in poslednji:
                                if i not in poslednji_num:
                                    poslednji_slovo = i
                            print("Posl_slovo: ", poslednji_slovo)
                            poslednje_slovo = translit(poslednji_slovo, 'sr', reversed=True)
                            # if '/' in poslednje_slovo:
                            #     for i in range(1, poslednje_slovo[-1])
                            #     poslednje_slovo = poslednje

                            poslednje_slovo_index = alphabet.index(poslednje_slovo)
                            list_of_chars = alphabet[: poslednje_slovo_index]

                #           #formiranje brojeva koji su izmedju potencijalno
                            for char in list_of_chars:
                                broj_ulaza = poslednji_num + char
                                final_list[ulica + " " + broj_ulaza] = ulica + " " + broj_ulaza
                            final_list[ulica + " " + poslednji] = ulica + " " + poslednji
                        else:
                            final_list[ulica + " " + poslednji] = ulica + " " + poslednji
                            poslednji_num = poslednji
                        print ('poslednji_num: ', poslednji_num)

            #           #dodati brojeve izmedju na listu
                        # if not(pocetni_lower.islower() or poslednji_lower.islower()):
                        for i in range(int(pocetni_num) + 1, int(poslednji_num)):
                            final_list[ulica + " " + str(i)] = ulica + " " + str(i)
                else:
                    final_list[ulica + " " + broj] = ulica + " " + broj

        #   else:
        #       #direktno kreiraj iskljucenje objekat
        #       pass

        # print ("Ulica: ", ulica)
        # print ("Brojevi: ", new_brojevi)
    return final_list

def buildingSearch(cuts):
    print ("Searching buildings")
    ulaz_list = []
    ulazi = Ulaz.objects.all()
    for ulaz in ulazi:
        if translit(ulaz.Ulica_i_broj.upper(), 'sr') in cuts.keys():
            print (ulaz)
            ulaz_list.append(ulaz)
    print ("Ulaz_list: ", ulaz_list)
    return ulaz_list

def sendEmails(buildings):
    print ("Sending emails")
    for building in buildings:
        for user in building.customuser_set.all():
            EMAIL_ADDRESS = "damircicic@gmail.com"
            password = "jpjpqiomgxbqustb"
            receiver = user.email
            msg = EmailMessage()
            msg['Subject'] = "Obaveštenje o isključenju struje."
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = receiver
            content = f"Zdravo {user.username}! Obaveštavamo vas da sutra u jednom delu dana nećete imati struju."
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


cuts = energyCuts('Чукарица')

buildings = buildingSearch(cuts)

sendEmails(buildings)

    

# with open('out.csv', 'w') as f:
#     writer = csv.writer(f)
#     writer.writerows(final_list)




# match = soup.title.text

# print (match)

# match = soup.div ## grabs first div on the page

# ##This can also be done like this:

# match =  soup.find('div')

# ##Match div with special class:
# match =  soup.find('div'. class_='footer') ##class_ because class is a keyword in python

# ##Get first article tag
# article = soup.find('div', class_i='article')

# print (article)

# ##Now search within the article for headlines

# headline = article.h2.a.text ##get text of p block

# summary = article.p.text
# print (headline)

# ##To find all articles in document, instead of using find, use find_all method.

# for article in soup.find_all('div', class_i='article')
