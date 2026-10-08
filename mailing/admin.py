from django.contrib import admin
from .models import Client, Mailing, Message, MailingLog
# Register your models here.

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'topic')

@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ('id', 'sending_date', 'status', 'periodicity')
    list_filter = ('status', 'periodicity')

@admin.register(MailingLog)
class MailingLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'status')