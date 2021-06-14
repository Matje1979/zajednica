from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MessageForUpravnik
from .forms import MessageReplyForm
from .serializers import MessageForUpravnikSerializer
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.

#This view actually for all users. MessageForUpravnik model despite the name is a model for all messages. Name needs to be changed.
class MessageListView(ListView):
    template_name = 'messaging/messages.html'
    context_object_name = 'usr_messages'
    paginate_by = 5
    def get_queryset(self):
        usr_messages = MessageForUpravnik.objects.filter(receiver=self.request.user)
        return usr_messages

#This the same as the previous, just using the DRF.
class CheckMessagesView(APIView):
    def get(self, request, pk):
        print ("Checking messages", flush=True)
        print ("PK: ", pk, flush=True)
        messages = MessageForUpravnik.objects.filter(receiver__id=int(pk))
        serializer = MessageForUpravnikSerializer(messages, many=True)
        print (messages, flush=True)
        # result = dict()
        # result['messages_num'] = len(messages)
        # result['user_messages'] = messages
        # print (result, flush=True)
        return Response(serializer.data)

class MngrMessageListView(ListView):
    # model = Post
    template_name = 'messaging/mngr_messages.html'
    context_object_name = 'msgs'
    paginate_by = 5
    def get_queryset(self, pk):
        print (self.request.user, flush=True)
        msgs = MessageForUpravnik.objects.filter(receiver=self.request.user)
        msgs = msgs.filter(sender__ulaz__id=pk)
        for msg in msgs:
            msg.seen = True
            msg.save()
        print (msgs, flush=True)
        return msgs
    # ordering = ['-date_posted']
    #for a ListView, default context object name is object_list, but that can be overriden in the way above.
    #for DetailView, defaul context object name is 'object'
class MsgDetailView(DetailView):
    model = MessageForUpravnik
    template_name = 'messaging/msg_detail.html'

    def get_context_data(self, **kwargs):
        context = super(MsgDetailView, self).get_context_data(**kwargs)
        msg = get_object_or_404(MessageForUpravnik, pk = self.kwargs['pk'])
        if msg:
            msg.read = True
            msg.save()
        context['msg'] = msg
        context['form'] = MessageReplyForm()
        # context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        c_form = MessageReplyForm(request.POST)
        if c_form.is_valid():
            obj = c_form.save(commit=False)
            obj.sender = self.request.user
            msg = get_object_or_404(MessageForUpravnik, pk = self.kwargs['pk'])
            receiver = msg.sender
            obj.receiver = receiver
            obj.save()
        return redirect('/manager_messages')


class MsgDeleteView(LoginRequiredMixin, DeleteView):

    model = MessageForUpravnik
    success_url='/manager_messages/'
