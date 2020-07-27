from django.contrib.auth import views as authviews
from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('hello/', views.hello, name='hello'),
]