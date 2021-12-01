from django.shortcuts import render

# Create your views here.

def events_home(request):
    return render(request, 'events/event_list.html')