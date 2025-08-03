from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Users(AbstractUser):

    def __str__(self):
        return self.username

    class Meta:
        db_table = "custom_users"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name="custom_user_set",
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name="custom_user_set",
        related_query_name="custom_user",
    )
