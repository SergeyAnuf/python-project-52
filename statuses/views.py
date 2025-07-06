from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import ProtectedError
from .models import Status
from .forms import StatusForm

class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/list.html'
    context_object_name = 'statuses'

class StatusCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/form.html'
    success_url = reverse_lazy('statuses:list')
    success_message = _('Status created successfully')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Create status')
        return context

class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'statuses/form.html'
    success_url = reverse_lazy('statuses:list')
    success_message = _('Status updated successfully')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Update status')
        return context

class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_url = reverse_lazy('statuses:list')
    success_message = _('Status deleted successfully')
    error_message = _('Cannot delete status because it is in use')

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            messages.success(self.request, self.success_message)
            return response
        except ProtectedError:
            messages.error(self.request, self.error_message)
            return self.render_to_response(self.get_context_data())