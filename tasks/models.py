from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from statuses.models import Status

class Task(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=_('Name')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created at')
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='authored_tasks',
        verbose_name=_('Author')
    )
    executor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name='assigned_tasks',
        blank=True,
        null=True,
        verbose_name=_('Executor')
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='tasks',
        verbose_name=_('Status')
    )
    labels = models.ManyToManyField(
        'labels.Label',
        related_name='tasks',
        blank=True,
        verbose_name=_('Labels')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
