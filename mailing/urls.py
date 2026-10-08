from django.urls import path
from mailing.apps import MailingConfig
from mailing.views import ClientListView, ClientDetailView, ClientCreateView, ClientUpdateView, ClientDeleteView

app_name = MailingConfig.name

urlpatterns = [
    path('', ClientListView.as_view(), name='clients'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('view/<int:pk>/', ClientDetailView.as_view(), name='client_view'),
    path('edit/<int:pk>/', ClientUpdateView.as_view(), name='client_edit'),
    path('delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
]
