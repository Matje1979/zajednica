import json
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MessageForUpravnik, MessageNotificationsBucket
from .forms import MessageReplyForm
from .serializers import MessageForUpravnikSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import Upravnik, CustomUser
from .forms import MessageForm
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.parsers import (
    MultiPartParser,
    FormParser,
    FileUploadParser,
)
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.authentication import (
SessionAuthentication,
BasicAuthentication
)

import json

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


# Create your views here.
class MarkSeenView(APIView):
    # Not sure if this plays any role
    # parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    authentication_classes = (
    CsrfExemptSessionAuthentication,
    BasicAuthentication
    )

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        # ulaz = Ulaz.objects.get(Ulica_i_broj=request.data['ulaz'])
        # This line is necessary because the field ulaz accepts
        # object ulaz not an address string
        id_dict = json.loads(request.data['new_seen'])
        for i in id_dict:
            msg = MessageForUpravnik.objects.get(id=i)
            msg.seen = True
            msg.save()
        # ulaz = Ulaz.objects.get(Ulica_i_broj=request.data["ulaz"])
        # if len(TempPapir.objects.filter(ulaz=ulaz)) == 0:
        #     serializer = PapirPrijavaSerializer(data=request.data)
        #     # flush=True seems necessary to be able to print
        #     # in console that is to get server logs in pythonanywhere

        #     if serializer.is_valid():
        #         try:
        #             # print (serializer, flush=True)
        #             # TempPapir.objects.create(
        #             # foto = serializer.validated_data['file'], ulaz = ulaz)

        #             # ulaz.box_full = False
        #             # ulaz.save()
        #             # serializer.save(ulaz=ulaz)
        #             # adding external argument ulaz to serializer
        #             serializer.save(ulaz=ulaz)
        #             return Response(
        #                 serializer.data, status=status.HTTP_201_CREATED
        #             )
        #         except KeyError:
        #             raise KeyError()
        #     return Response(
        #         serializer.errors, status=status.HTTP_400_BAD_REQUEST
        #     )
        # else:
        return Response(
                {"Success": "Hvala na prijavi! "}
            )
# This view actually for all users. MessageForUpravnik model.
# despite the name is a model for all messages. Name needs to be changed.
class MessageListView(ListView):
    template_name = 'messaging/inbox.html'
    context_object_name = 'usr_messages'
    paginate_by = 5
    def get_queryset(self):
        usr_messages = MessageForUpravnik.objects.filter(
            receiver=self.request.user
        )
        MessageNotificationsBucket.empty = True
        return usr_messages

    def get_context_data(self, **kwargs):
        context = super(MessageListView, self).get_context_data(**kwargs)
        context["upravnik"] = Upravnik.objects.get(ulaz=self.request.user.Ulaz)
        context["ulaz"] = self.request.user.Ulaz.Ulica_i_broj
        context["website"] = self.request.user.Ulaz.website
        context['msgs'] = MessageForUpravnik.objects.filter(
            sender=self.request.user
        )
        # MessageForUpravnik are all messages. Should change the name!
        messages = MessageForUpravnik.objects.filter(
            receiver=self.request.user
        )
        context["user_messages"] = messages
        context["page_title"] = "Primljene poruke"
        return context

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
        return msgs
    # ordering = ['-date_posted']
    #for a ListView, default context object name is object_list, but that can be overriden in the way above.
    #for DetailView, defaul context object name is 'object'
class MsgDetailView(DetailView):
    model = MessageForUpravnik
    template_name = 'messaging/msg_detail.html'

    def get_context_data(self, **kwargs):
        context = super(MsgDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_director == False:
            context["upravnik"] = Upravnik.objects.get(ulaz=self.request.user.Ulaz)
            context["ulaz"] = self.request.user.Ulaz.Ulica_i_broj
            context["website"] = self.request.user.Ulaz.website
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


class SentMessagesView(ListView):
    model = MessageForUpravnik
    template_name = 'messaging/sent_messages.html'
    context_object_name = 'msgs'
    paginate_by = 5

    def get_queryset(self):
        msgs = MessageForUpravnik.objects.filter(sender=self.request.user)

        return msgs

    def get_context_data(self, **kwargs):
        context = super(SentMessagesView, self).get_context_data(**kwargs)
        if self.request.user.is_director == False:
            context["upravnik"] = Upravnik.objects.get(ulaz=self.request.user.Ulaz)
            context["ulaz"] = self.request.user.Ulaz.Ulica_i_broj
            context["website"] = self.request.user.Ulaz.website
            context['usr_messages'] = MessageForUpravnik.objects.filter(
            receiver=self.request.user
        )

        return context

class MsgDeleteView(LoginRequiredMixin, DeleteView):

    model = MessageForUpravnik
    success_url='/messages_list/'


def create_message(request):
    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        if message_form.is_valid():
            new_message = message_form.save(commit=False)
            new_message.receiver = CustomUser.objects.get(id=request.POST['receiver'])
            new_message.sender = request.user
            new_message.save()
            messages.success(request, 'Poslali ste poruku!')

        ulaz = request.user.Ulaz.Ulica_i_broj
        context = {
            'ulaz': ulaz,
            'message_form': message_form}
        return render(request, 'messaging/inbox.html', context)
    else:
        message_form = MessageForm()
        ulaz = request.user.Ulaz.Ulica_i_broj
        context = {
            'ulaz': ulaz,
            'message_form': message_form}
        return render(request, 'messaging/create_message.html', context)


