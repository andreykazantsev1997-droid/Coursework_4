from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ClientForm, MessageForm, MailingForm
from .models import Client, Message, Mailing, MailingLog


# Create your views here.

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:clients')

class ClientListView(ListView):
    model = Client
    template_name = 'mailing/client_list.html'

class ClientDetailView(DetailView):
    model = Client

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:clients')

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:clients')

class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:messages')

class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'

class MessageDetailView(DetailView):
    model = Message

class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = 'mailing/message_form.html'
    success_url = reverse_lazy('mailing:messages')

class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:messages')

class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailings')

class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'

class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'

class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailings')

class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailings')

def mailing(request, pk):
    mailing = Mailing.objects.get(pk=pk)

    if timezone.now() < mailing.start_time or timezone.now() > mailing.end_time:
        messages.error(request, "Ошибка: время рассылки еще не наступило или уже прошло")
        return redirect('mailing:mailings')

    recipients = mailing.recipients.all()
    for recipient in recipients:
        try:
            send_mail(mailing.message.topic, mailing.message.text, settings.EMAIL_HOST_USER, [recipient.email])
            MailingLog.objects.create(mailing=mailing, status=True)

        except Exception as e:
            MailingLog.objects.create(mailing=mailing, status=False, answer=str(e))

    messages.success(request, "Рассылка успешно выполнена")
    return redirect('mailing:mailings')