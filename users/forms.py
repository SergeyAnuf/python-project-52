from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {
            'username': _('Имя пользователя'),
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
            'email': _('Email'),
        }
        help_texts = {
            'username': _('Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.'),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['password1'].label = _('Пароль')
            self.fields['password2'].label = _('Подтверждение пароля')
            self.fields['password1'].help_text = _('Ваш пароль должен содержать как минимум 8 символов.')