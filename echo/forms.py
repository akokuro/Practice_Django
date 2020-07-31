from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.forms import ModelForm


class RegisterUserForm(ModelForm):
    """Модель формы регистрации"""
    class Meta:
        model = User
        fields = ['username', 'password']
        help_texts = {
            'username': _('The username must contain from 6 to 12 characters and consist of English letters or numbers.'),
            'password': _('The password must contain from 6 to 12 characters and consist of English letters or numbers.'),
        }


class LoginUserForm(ModelForm):
    """Модель формы авторизации"""
    class Meta:
        model = User
        fields = ['username', 'password']
