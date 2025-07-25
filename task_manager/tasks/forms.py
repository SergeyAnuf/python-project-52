from django import forms
from django.contrib.auth import get_user_model
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class TaskForm(forms.ModelForm):
    executor = forms.ModelChoiceField(
        queryset=get_user_model().objects.all(),
        required=False,
        label=_('Executor'),  # Используем стандартный перевод
        widget=forms.Select(attrs={
            'class': 'form-select',
            'id': 'id_executor'
        })
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'status': _('Status'),
            'executor': _('Executor'),  # Стандартный перевод
        }