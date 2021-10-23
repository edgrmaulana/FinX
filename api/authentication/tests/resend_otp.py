from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

data = {
    'email': 'fauziladzuardhi6102@gmail.com',
    'phone_number': '6283135560460',
    'password': 'fauzi123#',
    'full_name': 'Fauzi Ladzuardhi Rokhmana',
}

phone = {
    'phone_number': '6283135560460'
}

class ResendOTPTestCase(APITestCase):
    '''Test all Resend OTP scenario'''
    url_register = reverse('authentication:register-list')
    url_resend_otp = reverse('authentication:resend-otp-list')

    def test_registered_phone_number(self):
        '''Resend OTP if the phone number is registered'''
        self.client.post(self.url_register, data, format='json')
        response = self.client.post(self.url_resend_otp, phone, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unregistered_phone_number(self):
        '''Resend OTP if the phone number is not registered'''
        response = self.client.post(self.url_resend_otp, phone, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)