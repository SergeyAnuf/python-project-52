from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Users(AbstractUser):
    # ... другие поля, если есть ...

    def __str__(self):
        if self.get_full_name():
            return self.get_full_name()
        return self.username

    class Meta:
        db_table = "custom_users"
        verbose_name = _("user")
        verbose_name_plural = _("users")
        # Добавьте related_name для разрешения конфликтов
        permissions = [
            ("can_manage_users", "Can manage users"),
        ]

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="custom_user_set",
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="custom_user_set",
        related_query_name="custom_user",
    )
