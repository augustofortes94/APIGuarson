from django.test import TestCase

# Create your tests here.
"""
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from .views import ApiLogin
import json
import pdb

class UserTestCase(APITestCase):
    def setUp(self):
        User.objects.create(
            first_name='test',
            last_name='test',
            email='test@test.com',
            username='testing_login',
            password='admin123',
        )

        self.login_url = '/login/'

        response = self.client.post(self.login_url, {'username':'testing_login', 'password':'admin123'})
        pdb.set_trace()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
        #self.token = response.data['token']
        #self.client.credentials(HTTP_AUTHORIZATION='Bearer' + self.token)
        return super().setUp()

    def test_login(self):
        pass
"""