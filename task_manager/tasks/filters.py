from django import forms
import django_filters
from .models import Task
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class TaskFilter(django_filters.FilterSet):
    self_tasks = django_filters.BooleanFilter(
        method='filter_self_tasks',
        label=_('Только свои задачи'),
        widget=forms.CheckboxInput,
    )

    class Meta:
        model = Task
        fields = ['status', 'executor', 'labels']

    def __init__(self, *args, **kwargs):
        # Получаем request из kwargs
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        if self.request:
            self.filters['executor'].queryset = User.objects.all()
        else:
            # Если request не передан, используем пустой queryset
            self.filters['executor'].queryset = User.objects.none()

        print(f"TaskFilter initialized. Request: {self.request}, User: {self.request.user if self.request else None}")

    def filter_self_tasks(self, queryset, name, value):
        print(f"Filtering self_tasks. Value: {value}, Type: {type(value)}")

        # Проверяем значение чекбокса через GET-параметр
        raw_value = self.data.get('self_tasks')
        if raw_value == 'on' and self.request and self.request.user.is_authenticated:
            print(f"Applying filter for user: {self.request.user}")
            return queryset.filter(author=self.request.user)

        print("No self_tasks filter applied")
        return queryset