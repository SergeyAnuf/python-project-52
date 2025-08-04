from django import forms
import django_filters
from .models import Task
from task_manager.users.models import Users
from django.utils.translation import gettext_lazy as _


class TaskFilter(django_filters.FilterSet):
    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks',
        label=_('Только свои задачи'),
        widget=forms.CheckboxInput,
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels', 'self_tasks']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
        self.filters['executor'].queryset = Users.objects.all()

    def filter_self_tasks(self, queryset, name, value):
        if value and self.request and self.request.user.is_authenticated:
            return queryset.filter(author=self.request.user)
        return queryset