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

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['username', 'first_name', 'last_name']
        labels = {
            'username': _('Имя пользователя'),
            'first_name': _('Имя'),
            'last_name': _('Фамилия'),
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Убираем поля пароля
        if 'password1' in self.fields:
            del self.fields['password1']
        if 'password2' in self.fields:
            del self.fields['password2']