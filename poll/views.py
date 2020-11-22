from django.shortcuts import render, redirect
from .forms import CreatePollForm

# Create your views here.
def home(request):
	ulaz = request.user.Ulaz.Ulica_i_broj
	context = {'ulaz': ulaz}
	return render(request, 'poll/poll_home.html', context)

def create(request):
	ulaz = request.user.Ulaz.Ulica_i_broj
	if request.method =='POST':
		form = CreatePollForm(request.POST)
		if form.is_valid():
			poll = form.save(commit=False)
			poll.author = request.user
			poll.save()
			return redirect('poll-home')
		
	else:
	    form = CreatePollForm()
	context = {'ulaz': ulaz, 'form': form}
	return render(request, 'poll/create.html', context)

def results(request, poll_id):
	context = {}
	return render(request, 'poll/results.html', context)

def vote(request, poll_id):
	context = {}
	return render(request, 'poll/vote.html', context)
