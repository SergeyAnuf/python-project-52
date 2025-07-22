from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from ..statuses.models import Status
from django.contrib.auth import get_user_model


User = get_user_model()


class Task(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    description = models.TextField(verbose_name=_('Description'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created at'))
    author = models.ForeignKey(
        User,
        related_name='authored_tasks',
        on_delete=models.CASCADE,
        verbose_name=_('Author')
    )
    executor = models.ForeignKey(
        User,
        related_name='assigned_tasks',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('Executor')
    )
    status = models.ForeignKey(
        'statuses.Status',  # Используем строковую ссылку для избежания циклических импортов
        on_delete=models.PROTECT,
        verbose_name=_('Status')
    )
    labels = models.ManyToManyField(
        'labels.Label',  # Используем строковую ссылку
        blank=True,
        related_name='tasks',
        verbose_name=_('Labels')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
