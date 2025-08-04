from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from .models import Users


class UserForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
        labels = {
            'username': _('Имя пользователя'),
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
        }
        help_texts = {
            'username': _('Обязательное поле. Не более 150 символов. Только буквы, цифры и символы @/./+/-/_.'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = _('Пароль')
        self.fields['password2'].label = _('Подтверждение пароля')
        self.fields['password1'].help_text = _('Ваш пароль должен содержать как минимум 3 символа.')
        self.fields['password2'].help_text = _('Для подтверждения введите, пожалуйста, пароль ещё раз.')

        # Убираем поле email
        if 'email' in self.fields:
            del self.fields['email']

        # Делаем имя и фамилию обязательными
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True