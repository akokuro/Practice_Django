from django.contrib.auth.models import User
from django.forms import ModelForm


class RegisterUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class LoginUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
