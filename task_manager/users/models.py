from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class Users(AbstractUser):
    # Убираем email как обязательное поле
    email = models.EmailField(_("email address"), blank=True, null=True)

    # Делаем имя и фамилию обязательными
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)

    def get_full_name(self):
        """Возвращает полное имя пользователя"""
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    def __str__(self):
        """Для отображения в выпадающих списках используем полное имя"""
        return self.get_full_name() or self.username

    class Meta:
        db_table = "custom_users"
        verbose_name = _("user")
        verbose_name_plural = _("users")

    # Остальное без изменений
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