from rest_framework.test import APITestCase
from django.test import Client
from django.urls import reverse
from rest_framework import status
from user.models import CustomUser
from rest_framework.authtoken.models import Token
from fixtures.factories import UserFactory, UserDataFactory

class AuthenticationTestCase(APITestCase):

    def setUp(self):
        self.client = Client()
        self.login_endpoint = reverse('login')
        self.register_endpoint = reverse('register')
        self.logout_endpoint = reverse('logout')


    def tearDown(self):
        CustomUser.objects.all().delete()



########################################################################
#          TEST CASES FOR LOGIN AND REGISTRATION OF USERS
#########################################################################


    def test_login(self):
        """Test login of user"""
        self.user = UserFactory()
        self.login_credentials = {"email":self.user.email, "password":"FakePassword123!*"}

        response = self.client.post(self.login_endpoint, self.login_credentials,format='json')
        self.user_token = Token.objects.get(user=self.user)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"token":self.user_token.key,"username":self.user.username,"email":self.user.email})


    def test_login_non_existent_user(self):
        """Test login of user with no account"""
  
        response = self.client.post(self.login_endpoint, {"email": "no_email@gmail.com", "password":"FakePassword456*+"},format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_one_user(self):
        """Test creation of new user"""

        fake_register_user_data = UserDataFactory()
        register_data= {"username":fake_register_user_data.username,"email":fake_register_user_data.email, "password":fake_register_user_data.password,"confirm_password":fake_register_user_data.password} 
        response = self.client.post(self.register_endpoint, register_data, format='json')

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertIn("email",response.data)
        self.assertIn("username",response.data)
        self.assertIn("token",response.data)
        self.assertEqual(len(CustomUser.objects.all()),1)


    def test_register_several_users(self):
        """Test creation of new user"""
   
        for _ in range(10):
            self.fake_user_data = UserDataFactory()
            register_data= {"username": self.fake_user_data.username,"email": self.fake_user_data.email, "password":self.fake_user_data.password,"confirm_password":self.fake_user_data.password} 
            response = self.client.post(self.register_endpoint, register_data, format='json')
            user = CustomUser.objects.get(username = self.fake_user_data.username)
            user_token = Token.objects.get(user=user)
            self.assertEqual(response.status_code,status.HTTP_201_CREATED)
            self.assertEqual(response.data, {"token": user_token.key,"username": user.username,"email": user.email})
        
        self.assertEqual(len(CustomUser.objects.all()),10)


    def test_register_bad_user_data(self):
        """Test creation of new user with bad data"""

        fake_register_user_data = UserDataFactory()
        register_data= {"username":fake_register_user_data.username,"email":fake_register_user_data.email, "password":fake_register_user_data.password,"confirm_password":"FakePassword133*+"} 

        response = self.client.post(self.register_endpoint, register_data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(CustomUser.objects.all()),0)


    def test_logout_user(self):
        """Test guest account deletion after user log out"""

        self.user = UserFactory()
        self.login_credentials = {"email":self.user.email, "password":"FakePassword123!*"}
      
        response = self.client.post(self.login_endpoint, self.login_credentials,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.logout_endpoint)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(CustomUser.objects.all()),1)

    def test_logout_guest(self):
        """Test guest account deletion after guest user log out"""

        self.login_credentials = {"email":"guest@videoflix.com", "password":"GuestPassword123!*"}

        response = self.client.post(self.login_endpoint, self.login_credentials,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.logout_endpoint)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(CustomUser.objects.all()),0)