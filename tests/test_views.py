from django.test import TestCase

# Create your tests here.

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from http.cookies import SimpleCookie
from django.urls import reverse

class UserListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        number_of_users = 5
        for author_num in range(number_of_users):
            name = 'Username%s' % author_num
            passwrod = 'password%s' % author_num
            user = User.objects.create(username=name)
            user.set_password(passwrod)
            user.save()

    def signup(self, name, password):
        resp = self.client.get('/signup/') 
        resp = self.client.post('/signup/', data={'username': name, 'password': password}) 
        return resp

    def login(self, name, password):
        resp = self.client.get('/login/') 
        resp = self.client.post('/login/', data={'username': name, 'password': password}) 
        return resp
           
    def test_view_url_signup(self): 
        resp = self.client.get('/signup/') 
        self.assertEqual(resp.status_code, 200)  
           
    def test_view_url_login(self):
        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code, 200)
        
    def test_unouthorithe_hello(self):
        resp = self.client.post('/hello/')
        self.assertEqual(resp.status_code, 401)

    def test_authorize_hello(self):
        resp = self.login('Username4', 'password4')
        resp = self.client.post('/hello/', data="Hello", content_type="text/html")
        self.assertEqual(resp.content, b'Hello')
    
    def test_correct_signup(self):
        resp = self.signup('Username6', 'password6')
        self.assertRedirects(resp, '/hello/')

    def test_correct_login(self):
        resp = self.login('Username4', 'password4')
        self.assertRedirects(resp, '/hello/')

    def test_incorrect_login(self):
        resp = self.login('Username7', 'password6')
        self.assertEqual(resp.status_code, 401)