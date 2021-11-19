from django.shortcuts import render, redirect
from .forms import CreatePollForm
from .models import Poll
from django.http import HttpResponse
from users.models import CustomUser
from django.contrib import messages

# Create your views here.
def home(request):
    ulaz = request.user.Ulaz.Ulica_i_broj
    polls = Poll.objects.all().order_by('-date_created')
    page_title = "Aktivne ankete"
    context = {'page_title': page_title, 'ulaz': ulaz, 'polls': polls}
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
    ulaz = request.user.Ulaz.Ulica_i_broj
    poll = Poll.objects.get(pk=poll_id)
    total = 0
    total += poll.ption_one_count
    total += poll.ption_two_count
    total += poll.ption_three_count

    context = {'total': total, 'poll': poll, 'ulaz': ulaz}
    return render(request, 'poll/results.html', context)

def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    user = CustomUser.objects.get(id=request.user.id)

    if request.method == 'POST':
        selected_option = request.POST['poll']
        print (poll)
        print (user.poll_set.all())
        if poll not in user.poll_set.all():
            print (poll not in user.poll_set.all())
            if selected_option == 'option1':
                poll.ption_one_count += 1
            elif selected_option == 'option2':
                poll.ption_two_count += 1
            elif selected_option == 'option3':
                poll.ption_three_count += 1
            else:
                pass
            # return HttpResponse(400, 'Invalid form')
            poll.save()
            poll.voters.add(user)
            return redirect('poll-results', poll_id)
        else:
            messages.info(request, f'Već ste glasali!.')
            ulaz = request.user.Ulaz.Ulica_i_broj
            context = {'poll':poll, 'ulaz':ulaz}
    else:
        ulaz = request.user.Ulaz.Ulica_i_broj
        poll = Poll.objects.get(id=poll_id)
        context = {'poll':poll, 'ulaz':ulaz}
    return render(request, 'poll/vote.html', context)
