from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView
from mailing.views import MessageListView, MessageCreateView, MessageDeleteView, MessageDetailView, MessageUpdateView

app_name = MailingConfig.name

urlpatterns = [
    path('', ClientListView.as_view(), name='clients'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('view/<int:pk>/', ClientDetailView.as_view(), name='client_view'),
    path('edit/<int:pk>/', ClientUpdateView.as_view(), name='client_edit'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    path('messages/', MessageListView.as_view(), name='messages'),
    path('messages/create/', MessageCreateView.as_view(), name='message_create'),
    path('messages/view/<int:pk>/', MessageDetailView.as_view(), name='message_view'),
    path('messages/edit/<int:pk>/', MessageUpdateView.as_view(), name='message_edit'),
    path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='message_delete'),
]
