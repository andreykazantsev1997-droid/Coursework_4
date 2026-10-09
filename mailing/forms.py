from django import forms
from .models import Client, Message, Mailing
from django.utils import timezone

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'comment']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['topic', 'text']

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'

class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('start_time', 'end_time', 'periodicity', 'message', 'recipients')
        widgets = {
            'start_time': forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and start_time < timezone.now():
            raise forms.ValidationError("Дата начала рассылки не может быть в прошлом!")

        if start_time and end_time and start_time > end_time:
            raise forms.ValidationError("Дата начала должна быть раньше даты окончания!")

        return cleaned_data
