from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext as _
from .forms import UserForm, UserUpdateForm  # Импортируем обе формы
from .models import Users
from task_manager.tasks.models import Task

class UserListView(ListView):
    model = Users
    template_name = 'users/list.html'
    context_object_name = 'users'

class UserCreateView(CreateView):
    model = Users
    form_class = UserForm  # Используем форму создания
    template_name = 'users/form.html'
    success_url = reverse_lazy('login')
    success_message = _('Пользователь успешно зарегистрирован!')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, self.success_message)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Регистрация')
        return context

class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Users
    form_class = UserUpdateForm  # Используем форму обновления
    template_name = 'users/form.html'
    success_url = reverse_lazy('users:users')
    success_message = _('Пользователь успешно изменен!')

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != self.get_object().pk:
            messages.error(request, _('У вас нет прав для изменения другого пользователя.'))
            return redirect('users:users')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Изменить пользователя')
        return context

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = Users
    template_name = 'users/delete.html'
    success_url = reverse_lazy('users:users')
    success_message = _('Пользователь успешно удален!')
    error_message = _('Невозможно удалить пользователя, потому что он связан с задачей')

    def dispatch(self, request, *args, **kwargs):
        if request.user.pk != self.get_object().pk:
            messages.error(request, _('У вас нет прав для изменения другого пользователя.'))
            return redirect('users:users')
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if Task.objects.filter(author=user).exists() or Task.objects.filter(executor=user).exists():
            messages.error(request, self.error_message)
            return redirect(self.success_url)
        messages.success(request, self.success_message)
        return self.delete(request, *args, **kwargs)

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Вы залогинены'))
        return response

    def get_success_url(self):
        return reverse_lazy('home')

def custom_logout(request):
    logout(request)
    messages.success(request, _('Вы разлогинены'))
    return redirect('home')