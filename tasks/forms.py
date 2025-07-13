from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from .models import Task
from statuses.models import Status
from labels.models import Label  # Добавляем импорт модели Label

User = get_user_model()


class TaskForm(forms.ModelForm):
#    labels = forms.ModelMultipleChoiceField(
#        queryset=Label.objects.all(),  # Теперь Label определен
#        required=False,
#        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
#        label=_('Метка')
#    )

    class Meta:
        model = Task
        fields = ['name', 'description', 'status', 'executor', 'labels']
        labels = {
            'name': _('Имя'),
            'description': _('Содержание'),
            'status': _('Статус'),
            'executor': _('Исполнитель'),
            'labels': _('Метка'),
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'executor': forms.Select(attrs={'class': 'form-select'}),
            'labels': forms.SelectMultiple(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['status'].queryset = Status.objects.all()
        self.fields['executor'].queryset = User.objects.all()
        # Теперь Label определен, поэтому эта строка будет работать
        self.fields['labels'].queryset = Label.objects.all()
        self.fields['labels'].label = _('Метка')