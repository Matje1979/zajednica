from django.shortcuts import render
from .models import PhoneCategory, PhoneNumber
from django.http import JsonResponse
from django.core import serializers

# Create your views here.
def phoneslist(request):
    phone_categories = PhoneCategory.objects.all()
    context = {"categories": phone_categories}
    return render(request, "phonebook/telefoni.html", context)

def get_phone_numbers(request, pk):
    phone_nums = PhoneNumber.objects.filter(category__pk=pk)
    phone_qs = serializers.serialize("json", phone_nums)
    return JsonResponse(phone_qs, safe=False)