from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenVerifySerializer
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.shortcuts import render
import jwt

from .forms import RegisterUserForm, LoginUserForm


def signup(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.data['password'])
            user.save()
            user = authenticate(username=form.data['username'], password=form.data['password'])
            return redirect('/hello/')
    else:
        form = RegisterUserForm()
    return render(request,
                  'registration/register.html',
                  {
                      'form': form
                  })


def login(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        user = authenticate(username=form.data['username'], password=form.data['password'])
        token = TokenObtainPairSerializer().get_token(user)
        response = HttpResponseRedirect('/hello/')
        response.set_cookie(key="jwt", value=token)
        return response
    else:
        form = LoginUserForm()
    return render(request,
                  'registration/login.html',
                  {
                      'form': form
                  })

def hello(request):
    if 'jwt' in request.COOKIES:
        data = request.COOKIES['jwt']
        try:
            decodedPayload = jwt.decode(str(data),None,None)   
            id = decodedPayload.get("user_id")
            if :
                return HttpResponse("Hello")
        except Exception:
            raise
            return HttpResponse("", status="401")
    return HttpResponse("", status="401")