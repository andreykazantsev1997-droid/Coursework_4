from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import ClientListView, ClientCreateView, ClientUpdateView, ClientDeleteView, toggle_mailing_active
from mailing.views import MessageListView, MessageCreateView, MessageDeleteView, MessageUpdateView
from mailing.views import MailingListView, MailingCreateView, MailingDeleteView, MailingUpdateView, mailing, MainMenuView
from django.views.decorators.cache import cache_page

app_name = MailingConfig.name

urlpatterns = [
    path('clients/', ClientListView.as_view(), name='clients'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('edit/<int:pk>/', ClientUpdateView.as_view(), name='client_edit'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('messages/', MessageListView.as_view(), name='messages'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/edit/<int:pk>/', MessageUpdateView.as_view(), name='messages_edit'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='messages_delete'),
    path('mailings/', MailingListView.as_view(), name='mailings'),
    path('mailings/create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailings/edit/<int:pk>/', MailingUpdateView.as_view(), name='mailing_edit'),
    path('mailings/delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailings/run/<int:pk>/', mailing, name='mailing_run'),
    path('mailings/toggle/<int:pk>/', toggle_mailing_active, name='toggle_mailing_active'),
    path('', cache_page(60)(MainMenuView.as_view()), name='home'),
]
