from django import forms
from django.contrib.auth import get_user_model
from .models import Task
from task_manager.statuses.models import Status
from task_manager.labels.models import Label
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class TaskForm(forms.ModelForm):
    labels = forms.ModelMultipleChoiceField(
        queryset=Label.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label=_('Labels')
    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'name': _('Name'),
            'description': _('Description'),
            'status': _('Status'),
            'executor': _('Executor'),
        }

    def __init__(self, *args, **kwargs):
        # Извлекаем user из kwargs перед вызовом super()
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Обновляем queryset'ы с учетом пользователя (если нужно)
        self.fields['executor'].queryset = User.objects.all()
        self.fields['status'].queryset = Status.objects.all()

        # Улучшаем отображение полей
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['status'].widget.attrs.update({'class': 'form-select'})
        self.fields['executor'].widget.attrs.update({'class': 'form-select'})