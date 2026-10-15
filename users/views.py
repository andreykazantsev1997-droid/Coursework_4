import secrets

from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
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

class UserListView(ListView):
    model = User
    template_name = 'users/user_list.html'
    def test_func(self):

        is_in_manager_group = self.request.user.groups.filter(name='managers').exists()
        return is_in_manager_group or self.request.user.is_superuser

@user_passes_test(lambda u: u.is_manager or u.is_superuser)
def toggle_user_active(request, pk):
    user_item = get_object_or_404(User, pk=pk)

    if not user_item.is_superuser and user_item != request.user:
        user_item.is_active = not user_item.is_active
        user_item.save()
    return redirect('users:user_list')
