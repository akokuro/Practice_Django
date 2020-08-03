from django.test import TestCase

# Create your tests here.

from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from http.cookies import SimpleCookie
from django.urls import reverse

class UserListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        """Настройка контекста для теста"""
        number_of_users = 5
        for author_num in range(number_of_users):
            name = 'Username%s' % author_num
            passwrod = 'password%s' % author_num
            user = User.objects.create(username=name)
            user.set_password(passwrod)
            user.save()

    def signup(self, name, password):
        """Регистрация пользователя с именем name и паролем password"""
        resp = self.client.get('/signup/') 
        resp = self.client.post('/signup/', data={'username': name, 'password': password}) 
        return resp

    def login(self, name, password):
        """Авторизация пользователя с именем name и паролем password"""
        resp = self.client.get('/login/') 
        resp = self.client.post('/login/', data={'username': name, 'password': password}) 
        return resp
           
    def test_view_url_signup(self): 
        """Тестирование получения формы регистрации"""
        resp = self.client.get('/signup/') 
        self.assertEqual(resp.status_code, 200)  
           
    def test_view_url_login(self):
        """Тестирование получения форму авторизации"""
        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code, 200)
        
    def test_unouthorithe_hello(self):
        """Тестирование обращения по адресу hello не авторизованным пользователем"""
        resp = self.client.post('/hello/')
        self.assertEqual(resp.status_code, 401)

    def test_authorize_hello(self):
        """Тестирование обращения по адресу hello с возвратом данных авторизованным пользователем"""
        resp = self.login('Username4', 'password4')
        resp = self.client.post('/hello/', data="Hello", content_type="text/html")
        self.assertEqual(resp.content, b'Hello')
    
    def test_correct_signup(self):
        """Тестирование регистрации пользователя с корректными данными"""
        resp = self.signup('Username6', 'password6')
        self.assertRedirects(resp, '/hello/')

    def test_correct_login(self):
        """Тестирование авторизации пользователя с корректными данными"""
        resp = self.login('Username4', 'password4')
        self.assertRedirects(resp, '/hello/')

    def test_incorrect_login(self):
        """Тестирование автризации несуществущего пользователя"""
        resp = self.login('Username7', 'password6')
        self.assertEqual(resp.status_code, 401)

    def test_signup_with_exists_username(self):
        """Тестирование регистрации существующего пользователя"""
        resp = self.signup('Username4', 'password6')
        self.assertEqual(resp.status_code, 403)

    def test_signup_with_incorrect_credentials(self):
        """Тестирование регистрации пользователя с несоответствующими шаблону данными"""
        self.client.raise_request_exception = True
        # Логин больше 12 символов
        with self.assertRaises(ValidationError):
            resp = self.signup('Username412313432113', 'password6')
        # Пароль больше 12 символов
        with self.assertRaises(ValidationError):
            resp = self.signup('Username7', 'password63875389310')
        # Логин меньше 6 символов
        with self.assertRaises(ValidationError):
            resp = self.signup('User', 'password6')
        # Пароль меньше 6 символов
        with self.assertRaises(ValidationError):
            resp = self.signup('Username41', 'pass')
        # Логин состоит не только из английских букв и цифр
        with self.assertRaises(ValidationError):
            resp = self.signup('Username4!', 'password6')
        # Пароль состоит не только из английский букв и цифр
        with self.assertRaises(ValidationError):
            resp = self.signup('Username10', 'password!')
            
    def test_signup_authogenerate_credentials(self):
        """Тестирование регистрации автосгенерированного пользователя"""
        resp = self.client.get('/signup/?thinkforme=true') 
        self.assertEqual(resp.status_code, 200)

    
