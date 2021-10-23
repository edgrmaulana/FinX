from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from enterprise.structures.authentication.models import PhoneVerification

data = {
    'email': 'fauziladzuardhi6102@gmail.com',
    'phone_number': '6283135560460',
    'password': 'fauzi123#',
    'full_name': 'Fauzi Ladzuardhi Rokhmana'
}

class VerifyPhoneTestCase(APITestCase):
    '''Test all phone number verification scenario'''
    url_phone = reverse("authentication:verify-phone-list")
    url_register = reverse("authentication:register-list")

    def test_valid_phone_verification_code(self):
        '''Test valid phone number'''
        self.client.post(self.url_register, data, format='json')
        pv = PhoneVerification.objects.filter(phone_number=data["phone_number"]).first()
        phone = {
            "phone_number": data["phone_number"],
            "code": pv.code
        }
        response = self.client.post(self.url_phone, phone, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_phone_number(self):
        '''Test invalid phone number'''
        self.client.post(self.url_register, data, format='json')
        phone = {
            "phone_number": '66666',
            "code": '061002'
        }
        response = self.client.post(self.url_phone, phone, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_phone_verification_code(self):
        '''Test invalid code'''
        self.client.post(self.url_register, data, format='json')
        phone = {
            "phone_number": data["phone_number"],
            "code": 'invalid_code'
        }
        response = self.client.post(self.url_phone, phone, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)