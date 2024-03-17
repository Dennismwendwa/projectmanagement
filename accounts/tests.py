from django.test import TestCase
from django.shortcuts import reverse
from django.contrib.auth.models import Group
from django.contrib.messages import get_messages
from .models import User


class AccountsRegisterView(TestCase):
    def test_register_new_user(self):
        url = reverse("accounts:register")

        data = {
            "first_name": "dennis",
            "last_name": "mwendwa",
            "username": "dennis",
            "email": "dennis@gmail.com",
            "password1": "1234567890",
            "password2": "1234567890",
            "role": "admin",
        }

        response = self.client.post(url, data)
        user = User.objects.get(username="dennis")
        
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("accounts/register")
        self.assertTrue(user.groups.filter(name=f"{data['role'].capitalize()}").exists())
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(user.is_authenticated)

    def test_register_with_existing_username(self):
        url = reverse("accounts:register")

        data = {
            "first_name": "dennis",
            "last_name": "mwendwa",
            "username": "dennis",
            "email": "dennis@gmail.com",
            "password1": "1234567890",
            "password2": "1234567890",
            "role": "admin",
        }
        respons = self.client.post(url, data)
        response = self.client.post(url, data)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level_tag, 'warning')
        self.assertEqual(str(messages[0]), "Username already taken")

    def test_register_with_existing_email(self):
        url = reverse("accounts:register")

        data = {
            "first_name": "dennis",
            "last_name": "mwendwa",
            "username": "dennis",
            "email": "dennis@gmail.com",
            "password1": "1234567890",
            "password2": "1234567890",
            "role": "admin",
        }
        data1 = {
            "first_name": "dennis",
            "last_name": "mwendwa",
            "username": "muse",
            "email": "dennis@gmail.com",
            "password1": "1234567890",
            "password2": "1234567890",
            "role": "admin",
        }
        respons = self.client.post(url, data)
        response = self.client.post(url, data1)
        messages = list(get_messages(response.wsgi_request))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level_tag, 'warning')
        self.assertEqual(str(messages[0]), "Email already in use")
        self.assertEqual(User.objects.count(), 1)
    
    def test_register_with_short_password(self):
        url = reverse("accounts:register")

        data = {
            "first_name": "dennis",
            "last_name": "mwendwa",
            "username": "dennis",
            "email": "dennis@gmail.com",
            "password1": "1234567",
            "password2": "1234567890",
            "role": "admin",
        }

        response = self.client.post(url, data)
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level_tag, 'warning')
        self.assertEqual(str(messages[0]), "Password MUST have minimum of 8 characters!")

    def test_register_with_not_matching_password(self):
        url = reverse("accounts:register")

        data = {
            "first_name": "dennis",
            "last_name": "mwendwa",
            "username": "dennis",
            "email": "dennis@gmail.com",
            "password1": "123456789000",
            "password2": "1234567890",
            "role": "admin",
        }

        response = self.client.post(url, data)

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].level_tag, 'warning')
        self.assertEqual(str(messages[0]), "Password not matching")


class AccountsLoginView(TestCase):
    def setUp(self) -> None:
        User.objects.create_user(
            first_name="dennis",
            last_name="mwendwa",
            email="dennis@gmail.com",
            username="dennis",
            password="den666666",
        )
    
    def test_successfull_login(self):
        url = reverse("accounts:login")

        data = {
            "username": "dennis",
            "password": "den666666"
        }

        response = self.client.post(url, data)
        user = User.objects.get(username=f"{data['username']}")
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed("accounts/login.html")
        self.assertTrue(user.is_authenticated)

    def test_login_with_missing_username(self):
        url = reverse("accounts:login")
        data = {
            "username": "dennis",
            "password": ""
        }

        response = self.client.post(url, data)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(response.status_code, 302)
        self.assertTemplateUsed("accounts/login.html")
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Please enter both username and password")

    def test_login_with_wrong_password(self):
        url = reverse("accounts:login")
        data = {
            "username": "dennis",
            "password": "5566"
        }

        response = self.client.post(url, data)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed("accounts/login.html")
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid username or password")


class AccountsLogout(TestCase):
    def setUp(self) -> None:
        url = reverse("accounts:register")

        data = {
            "first_name": "dennis",
            "last_name": "mwendwa",
            "username": "dennis",
            "email": "dennis@gmail.com",
            "password1": "1234567890",
            "password2": "1234567890",
            "role": "admin",
        }

        response = self.client.post(url, data)
    
    def test_logout(self):
        url = reverse("accounts:logout")

        self.assertIn('_auth_user_id', self.client.session)
        response = self.client.get(url)
        self.assertNotIn('_auth_user_id', self.client.session)
