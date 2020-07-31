from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render
import jwt

from .forms import RegisterUserForm, LoginUserForm


def redirect_with_jwt(path, token):
    """Перенаправление на страницу path с добавлением jwt-токена token в куки"""
    response = HttpResponseRedirect(path)
    response.set_cookie(key="jwt", value=token)
    return response


def get_token(name, password):
    """Возвращает jwt-токен для пользователя с логином name и паролем password
    Возвращает None, если такого пользователя не существует"""
    user = authenticate(username=name, password=password)
    if user:
        token = TokenObtainPairSerializer().get_token(user)
        return token
    else:
        return None


def signup(request):
    """Представление регистрации
    Регистрирует пользователя, если пароль и логин состоят из английских букв и цифр и их длина находится в диапазоне [6;12]
    Если нет, то выдает ошибку ValidationError, пользователю показывается сообщение: "Password or login is incorrect."
    Если пользователь с введенным логином существует, то пользователю вернется ошибка 403 с сообщением:"This login is already used"
    Если в строке запроса был передан параметр thinkforme со значением True, то пользователь регистрируется слуайным логином и паролем,
    которые возвращаются в ответ на запрос"""
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            if  6 <= len(form.data['password']) <= 12 and \
                6 <= len(form.data['username']) <= 12 and \
                form.data['username'].isalnum() and form.data['password'].isalnum():

                user = form.save(commit=False)
                user.set_password(form.data['password'])
                user.save()
                token = get_token(form.data['username'], form.data['password'])
                if token == None:
                    return HttpResponse('Unauthorized', status=401)
                else:
                    return redirect_with_jwt('/hello/', token)
            else:
                raise ValidationError(
                    _('Password or login is incorrect.'),
                )
        else:
            return HttpResponse('This login is already used', status=403)
    if 'thinkforme' in request.GET and request.GET['thinkforme'] == 'true':
        name = User.objects.make_random_password()
        passwrod = User.objects.make_random_password()
        user = User.objects.create_user(username=name)
        user.set_password(passwrod)
        user.save()
        return HttpResponse('Your username is ' + name + ' your password is ' + passwrod, status=200)
    return render(request,
                  'registration/register.html',
                  {
                      'form': RegisterUserForm()
                  })


def login(request):
    """Представление авторизации
    Авторизует пользователя и перенаправляет его на страницу 'hello', если полученные логин и пароль существуют в базе данных
    Возвращает ошибку 401, если такого пользователя не существует"""
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        token = get_token(form.data['username'], form.data['password'])
        if token == None:
            return HttpResponse('Unauthorized', status=401)
        else:
            return redirect_with_jwt('/hello/', token)
    else:
        form = LoginUserForm()
    return render(request,
                  'registration/login.html',
                  {
                      'form': form
                  })

def hello(request):
    """Возвращает тело запроса, если пользователь авторизован
    Возвращает ошибку 401, если пользователь не авторизован"""
    if 'jwt' in request.COOKIES:
        if request.method == 'POST':
            data = request.COOKIES['jwt']
            try:
                decodedPayload = jwt.decode(str(data),None,None)   
                id = decodedPayload.get("user_id")
                return HttpResponse(request.body, status=200)
            except Exception:
                return HttpResponse("", status=401)
        else:
            return HttpResponse("Hello", status=200)
    return HttpResponse("", status=401)
