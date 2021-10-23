from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from enterprise.structures.authentication.models import PhoneVerification, EmailVerification

data = {
    'email': 'fauziladzuardhi6102@gmail.com',
    'phone_number': '6283135560460',
    'password': 'fauzi123#',
    'full_name': 'Fauzi Ladzuardhi Rokhmana'
}

class LoginTestCase(APITestCase):
    '''Test all login scenario'''
    url_login = reverse('authentication:authenticate-password-list')
    url_register = reverse('authentication:register-list')
    url_phone = reverse('authentication:verify-phone-list')
    url_email = reverse('authentication:verify-email-list')

    def test_verified_login(self):
        '''Tes valid email with verified account'''
        self.client.post(self.url_register, data, format='json')

        phone_verification = PhoneVerification.objects.filter(phone_number=data['phone_number']).first()
        phone = {
            'phone_number': data['phone_number'],
            'code': phone_verification.code
        }
        self.client.post(self.url_phone, phone, format='json')

        email_verification = EmailVerification.objects.filter(email=data['email']).first()
        email = {
            'email': data['email'],
            'code': email_verification.code_hash
        }
        self.client.post(self.url_email, email, format='json')

        login = {
            'email': data['email'],
            'password': data['password']
        }
        response = self.client.post(self.url_login, login, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['register_status'], {
            'phone': True,
            'email': True,
            'profile': False
        })

    def test_login_without_verification(self):
        '''Tes valid email without verified account'''
        self.client.post(self.url_register, data, format='json')

        login = {
            'email': data['email'],
            'password': data['password']
        }
        response = self.client.post(self.url_login, login, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['register_status'], {
            'phone': False,
            'email': False,
            'profile': False
        })

    def test_invalid_email(self):
        '''Tes invalid email'''
        login = {
            'email': data['email'],
            'password': data['password']
        }
        response = self.client.post(self.url_login, login, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_password(self):
        '''Tes invalid password'''
        self.client.post(self.url_register, data, format='json')

        login = {
            'email': data['email'],
            'password': 'invalid'
        }
        response = self.client.post(self.url_login, login, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)