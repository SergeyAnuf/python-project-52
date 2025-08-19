from django import forms
import django_filters
from .models import Task
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    self_tasks = django_filters.BooleanFilter(
        label=_('Только свои задачи'),
        widget=forms.CheckboxInput,
        method='filter_self_tasks',
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['executor'].queryset = User.objects.all()

    def filter_self_tasks(self, queryset, name, value):
        if (value and hasattr(self.request, 'user') and
            self.request.user.is_authenticated):
            return queryset.filter(author=self.request.user)
        return queryset