import secrets
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView
from .forms import UserRegisterForm, UserLoginForm
from .models import User
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('users:login')

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        url = f"http://127.0.0.1:8000/users/confirm-email/{token}/"
        try:
            send_mail(
                subject="Подтверждение регистрации",
                message=f"Для подтверждения регистрации перейдите по ссылке: {url}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
            )
        except Exception:
            pass
        return super().form_valid(form)

def confirm_email(request, token):
    try:
        user = User.objects.get(token=token)
        user.is_active = True
        user.token = None
        user.save()
    except Exception:
        pass
    return redirect('users:login')
