from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from enterprise.structures.authentication.models import User

data = {
    'email': 'fauziladzuardhi6102@gmail.com',
    'phone_number': '6283135560460',
    'password': 'fauzi123#',
    'full_name': 'Fauzi Ladzuardhi Rokhmana'
}

class RegisterTestCase(APITestCase):
    '''Test all register scenario'''
    url = reverse('authentication:register-list')

    def test_valid_registration(self):
        '''Valid registration'''
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phone_number'], data['phone_number'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['full_name'], data['full_name'])
        self.assertEqual(response.data['token'], Token.objects.get(
            user=User.objects.get(email=data['email'])).key)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_email_exist(self):
        '''Email already exist'''
        User.objects.create(email=data['email'],
                            phone_number='628815150127', 
                            full_name=data['full_name'])
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_phone_number_exist(self):
        '''Phone number already exist'''
        User.objects.create(email='fauzilrokhmana@gmail.com',
                            phone_number=data['phone_number'], 
                            full_name=data['full_name'])
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_payload(self):
        '''Mising payload'''
        data = {}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)