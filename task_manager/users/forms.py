from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import Users


# Форма для создания пользователя
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
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


# Форма для обновления пользователя (с полями пароля)
class UserUpdateForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
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
        # Делаем поля пароля необязательными
        self.fields['password1'].required = False
        self.fields['password2'].required = False

        # Настраиваем подсказки
        self.fields['password1'].label = _('Пароль')
        self.fields['password2'].label = _('Подтверждение пароля')
        self.fields['password1'].help_text = _(
            'Оставьте пустым, если не хотите менять пароль. Ваш пароль должен содержать как минимум 3 символа.')
        self.fields['password2'].help_text = _('Для подтверждения введите, пожалуйста, пароль ещё раз.')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Проверяем только если хотя бы одно поле пароля заполнено
        if password1 or password2:
            if password1 != password2:
                raise ValidationError(_("Пароли не совпадают"))

            # Валидация пароля
            try:
                validate_password(password1, self.instance)
            except ValidationError as e:
                self.add_error('password1', e)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)

        # Обновляем пароль только если он был указан
        if self.cleaned_data.get("password1"):
            user.set_password(self.cleaned_data["password1"])

        if commit:
            user.save()
        return user