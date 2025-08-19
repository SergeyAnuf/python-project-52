from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from .models import Label
from .forms import LabelForm
from task_manager.tasks.models import Task


class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/list.html'
    context_object_name = 'labels'


class LabelCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/form.html'
    success_url = reverse_lazy('labels:list')
    success_message = _('Метка успешно создана')


class LabelUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'labels/form.html'
    success_url = reverse_lazy('labels:list')
    success_message = _('Метка успешно изменена')


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'labels/delete.html'
    success_url = reverse_lazy('labels:list')
    success_message = _('Метка успешно удалена')
    error_message = _('Невозможно удалить метку, потому что она используется')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, _('Вы не авторизованы! Пожалуйста, войдите в систему.'))
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Убрали проверку использования метки из GET-контекста
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Проверяем, используется ли метка в задачах
        if Task.objects.filter(labels=self.object).exists():
            messages.error(request, self.error_message)
            return redirect(self.success_url)

        try:
            response = super().post(request, *args, **kwargs)
            messages.success(request, self.success_message)
            return response
        except ProtectedError:
            messages.error(request, self.error_message)
            return redirect(self.success_url)