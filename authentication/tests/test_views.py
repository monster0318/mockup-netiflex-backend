from rest_framework.test import APITestCase
from django.test import Client
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from user.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from fixtures.factories import UserFactory, UserDataFactory
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class AuthenticationViewTest(APITestCase):
    """Testing authentication views"""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.login_endpoint = reverse('login')
        cls.register_endpoint = reverse('register')
        cls.logout_endpoint = reverse('logout')


    def tearDown(self):
        User.objects.all().delete()

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
        self.assertEqual(response.data, {"token":self.user_token.key,"email":self.user.email})


    def test_login_non_existent_user(self):
        """Test login of user with no account"""
  
        response = self.client.post(self.login_endpoint, {"email": "no_email@gmail.com", "password":"FakePassword456*+"},format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_one_user(self):
        """Test creation of new user"""

        fake_register_user_data = UserDataFactory()
        register_data= {"email":fake_register_user_data.email, "password":fake_register_user_data.password,"confirm_password":fake_register_user_data.password} 
        response = self.client.post(self.register_endpoint, register_data, format='json')

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertIn("email",response.data)
        self.assertIn("token",response.data)
        self.assertEqual(len(User.objects.all()),1)


    def test_register_several_users(self):
        """Test creation of new user"""
   
        for _ in range(3):
            fake_user_data = UserDataFactory()
            register_data= {"username": fake_user_data.username,"email": fake_user_data.email, "password":fake_user_data.password,"confirm_password":fake_user_data.password} 
            response = self.client.post(self.register_endpoint, register_data, format='json')
            user = User.objects.get(email = register_data["email"])
            user_token = Token.objects.get(user=user)
            self.assertEqual(response.status_code,status.HTTP_201_CREATED)
            self.assertEqual(response.data, {"token": user_token.key,"email": user.email})
        
        self.assertEqual(len(User.objects.all()),3)


    def test_register_bad_user_data(self):
        """Test creation of new user with bad data"""

        fake_register_user_data = UserDataFactory()
        register_data= {"email":fake_register_user_data.email, "password":fake_register_user_data.password,"confirm_password":"FakePassword133*+"} 

        response = self.client.post(self.register_endpoint, register_data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(User.objects.all()),0)


    def test_logout_user(self):
        """Test guest account deletion after user log out"""

        self.user = UserFactory()
        self.login_credentials = {"email":self.user.email, "password":"FakePassword123!*"}
        self.client.login(email=self.user.email,password="FakePassword123!*")
        response = self.client.delete(self.logout_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(User.objects.all()),1)

    def test_logout_guest(self):
        """Test guest account deletion after guest user log out"""

        self.login_credentials = {"email":"guest@videoflix.com", "password":"GuestPassword123!*"}
        response = self.client.post(self.login_endpoint, self.login_credentials,format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.logout_endpoint)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(User.objects.all()),0)


    def test_activate_account_view_good_data(self):
        """Test account activation view with good credentials"""

        user = get_user_model().objects.create(email="testuser@gmail.com", password="password", is_active=False)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        url = reverse("activate-account")
        activation_credentials = {
            "uid": uid,
            "token":token
        }
        response = self.client.post(url,activation_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_activate_account_view_already_active_account(self):
        """Test account activation of already activated account"""

        user = UserFactory()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        url = reverse("activate-account")
        activation_credentials = {
            "uid": uid,
            "token":token
        }
        response = self.client.post(url,activation_credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("message"), "This account is already active. You can log in!")

    def test_activate_account_view_bad_data(self):
        """Test account activation view with bad credentials"""

        user = UserFactory()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(100))
        url = reverse("activate-account")
        activation_credentials = {
            "uid": uid,
            "token":token
        }
        response = self.client.post(url,activation_credentials, format='json')
        self.assertEqual(response.data.get("message")[0], "Invalid user ID or token")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reset_pwd_view_good_data(self):
        """Testing reset password view with good data"""

        user = UserFactory()
        url = reverse("reset-password")
        email_address = {
            "email":user.email,
            }
        response = self.client.post(url,email_address, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "Password reset link sent to your email!")
    
    def test_reset_pwd_view_bad_data(self):
        """Testing reset password view with non existing email"""

        user = UserFactory()
        url = reverse("reset-password")
        email_address = {
            "email":"test@gmail.com",
            }
        response = self.client.post(url,email_address, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("message")[0], "No account found with this email")

    def test_confirm_reset_pwd_view_good_data(self):
        """Testing confirm reset password view with good data"""

        user = UserFactory()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        url = reverse("confirm-reset-password")
        credentials = {
            "uid":uid,
            "token":token,
            "new_password":"Test456!",
            "confirm_new_password":"Test456!"
            }
        response = self.client.post(url,credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("message"), "Password successfully reset!")
    
    def test_confirm_reset_pwd_view_bad_data(self):
        """Testing confirm reset password view with non existing email"""

        user = UserFactory()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(100))
        url = reverse("confirm-reset-password")
        credentials = {
            "uid":uid,
            "token":token,
            "new_password":"Test456!",
            "confirm_new_password":"Test456!"
            }
        response = self.client.post(url,credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("message")[0], "Invalid user ID or token")

    def test_confirm_reset_pwd_view_bad_passwords(self):
        """Testing confirm reset password view with no matching password"""

        user = UserFactory()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        url = reverse("confirm-reset-password")
        credentials = {
            "uid":uid,
            "token":token,
            "new_password":"Test456!",
            "confirm_new_password":"Test456789!"
            }
        response = self.client.post(url,credentials, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data.get("message")[0], "Passwords must match")
