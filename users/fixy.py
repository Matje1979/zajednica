import json
import time
import itertools
from users.models import Upravnik
with open('duplicate_fix.json') as f:
    data = json.load(f)
    for d in data.items():
        i = Upravnik.objects.get(ulaz__Ulica_i_broj = d[0])
        i.user.username = d[1] + "_@"
        i.save()
        print (d[1], " saved")
                
