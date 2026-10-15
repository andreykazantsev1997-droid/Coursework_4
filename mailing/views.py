from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .forms import ClientForm, MessageForm, MailingForm
from .models import Client, Message, Mailing, MailingLog


# Create your views here.

class MainMenuView(TemplateView):
    model = Mailing
    template_name = 'mailing/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['mailings_count'] = Mailing.objects.filter(user=self.request.user).count()
            context['clients_count'] = Client.objects.filter(mailing__user=self.request.user).distinct().count()
            context['active_mailings_count'] = Mailing.objects.filter(user=self.request.user, start_time__lte=timezone.now(), end_time__gte=timezone.now()).count()
            context['successful_plots'] = MailingLog.objects.filter(mailing__user=self.request.user, status=True).count()
            context['unsuccessful_plots'] = MailingLog.objects.filter(mailing__user=self.request.user, status=False).count()

        else:
            context['mailings_count'] = 0
            context['clients_count'] = 0
            context['active_mailings_count'] = 0
            context['successful_plots'] = 0
            context['unsuccessful_plots'] = 0

        return context

class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:clients')

class ClientListView(ListView):
    model = Client
    template_name = 'mailing/client_list.html'

    def get_queryset(self):
        if self.request.user.groups.filter(name='managers').exists() or self.request.user.is_superuser:
            return Client.objects.all()
        else:
            return Client.objects.filter(user=self.request.user)

class ClientDetailView(DetailView):
    model = Client

class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'mailing/client_form.html'
    success_url = reverse_lazy('mailing:clients')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        is_owner = obj.user == request.user

        if not (is_owner or request.user.is_superuser):
            return HttpResponseForbidden("У вас нет прав на редактирование этого клиента")

        return super().dispatch(request, *args, **kwargs)

class ClientDeleteView(DeleteView):
    model = Client
    template_name = 'mailing/client_confirm_delete.html'
    success_url = reverse_lazy('mailing:clients')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        is_owner = obj.user == request.user

        if not (is_owner or request.user.is_superuser):
            return HttpResponseForbidden("У вас нет прав на удаление этого клиента")

        return super().dispatch(request, *args, **kwargs)

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

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.user = self.request.user
        mailing.save()
        return super().form_valid(form)

class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'

    def get_queryset(self):
        if self.request.user.groups.filter(name='managers').exists() or self.request.user.is_superuser:
            return Mailing.objects.all()
        else:
            return Mailing.objects.filter(user=self.request.user)

class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'

class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailings')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        is_owner = obj.user == request.user

        if not (is_owner or request.user.is_superuser):
            return HttpResponseForbidden("У вас нет прав на редактирование этого сообщения")

        return super().dispatch(request, *args, **kwargs)

class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailings')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        is_owner = obj.user == request.user

        if not (is_owner or request.user.is_superuser):
            return HttpResponseForbidden("У вас нет прав на удаление этого сообщения")

        return super().dispatch(request, *args, **kwargs)

def mailing(request, pk):
    mailing = Mailing.objects.get(pk=pk)

    if timezone.now() < mailing.start_time or timezone.now() > mailing.end_time:
        messages.error(request, "Ошибка: время рассылки еще не наступило или уже прошло")
        return redirect('mailing:mailings')

    recipients = mailing.recipients.all()
    mailing.status = 'started'
    mailing.save()
    for recipient in recipients:
        try:
            send_mail(mailing.message.topic, mailing.message.text, settings.EMAIL_HOST_USER, [recipient.email])
            MailingLog.objects.create(mailing=mailing, status=True)

        except Exception as e:
            MailingLog.objects.create(mailing=mailing, status=False, server_response=str(e))

    messages.success(request, "Рассылка успешно выполнена")
    return redirect('mailing:mailings')

def is_manager_check(user):
    return user.is_manager or user.is_superuser

@user_passes_test(is_manager_check)
def toggle_mailing_active(request, pk):
    mailing = get_object_or_404(Mailing, pk=pk)
    if mailing.status == 'started':
        mailing.status = 'completed'
    else:
        mailing.status = 'started'

    mailing.save()
    return redirect('mailing:mailings')