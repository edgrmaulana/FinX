from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from enterprise.structures.authentication.models import EmailVerification

data = {
    'email': 'fauziladzuardhi6102@gmail.com',
    'phone_number': '6283135560460',
    'password': 'fauzi123#',
    'full_name': 'Fauzi Ladzuardhi Rokhmana'
}


class VerifyEmailTestCase(APITestCase):
    '''Test all email verification scenario'''
    url_register = reverse("authentication:register-list")
    url_email = reverse("authentication:verify-email-list")

    def test_valid_email_verification_code(self):
        '''Test valid code'''
        self.client.post(self.url_register, data, format='json')

        ev = EmailVerification.objects.filter(email=data["email"]).first()
        email = {
            "code": ev.code_hash
        }
        response = self.client.post(self.url_email, email, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_email_verification_code(self):
        '''Test invalid code'''
        self.client.post(self.url_register, data, format='json')

        email = {
            "code": "invalid_code"
        }
        response = self.client.post(self.url_email, email, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)