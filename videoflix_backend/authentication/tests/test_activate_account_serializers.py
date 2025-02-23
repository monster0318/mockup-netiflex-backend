from rest_framework.test import APITestCase, APIClient
from authentication.api.serializers import ActivateAccountSerializer
from user.models import CustomUser
from fixtures.factories import UserFactory
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class TestActivateAccountSerializer(APITestCase):
    """Testing activate account serializer"""
    
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

    def setUp(self):
        self.user = UserFactory()
        self.uid = urlsafe_base64_encode(force_bytes(self.user.id))
        self.token = default_token_generator.make_token(user = self.user) 
    
    def tearDown(self):
        CustomUser.objects.all().delete()



    def test_validate_activate_account_with_good_data(self):
        """Testing validate activate account with good data"""

        credentials = {
            "uid":self.uid,
            "token":self.token,
            }
        serializer = ActivateAccountSerializer(data = credentials)
        serializer.is_valid(raise_exception=True)
        credentials['user'] = self.user
        self.assertEqual(serializer.validated_data, credentials)
    
    def test_validate_activate_account_with_wrong_token(self):
        """Testing validate activate account with wrong token"""

        user2 = UserFactory()
        self.token = default_token_generator.make_token(user = user2) 
        credentials = {
            "uid":self.uid,
            "token":self.token,
            }
        serializer = ActivateAccountSerializer(data = credentials)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEqual({"type":context.exception.detail["type"][0],"message":context.exception.detail["message"][0]},{"type":"token","message":"Invalid or expired token"})
    
    def test_validate_activate_account_of_non_existing_user(self):
        """Testing validate activate account of non existing user"""

        self.uid = urlsafe_base64_encode(force_bytes(100))
        credentials = {
            "uid":self.uid,
            "token":self.token,
            }
        serializer = ActivateAccountSerializer(data = credentials)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEqual({"type":context.exception.detail["type"][0],"message":context.exception.detail["message"][0]},{"type":"token","message":"Invalid user ID or token"})
    
    def test_validate_save_activated_account(self):
        """Testing validate save activated account"""
     
        credentials = {
            "uid":self.uid,
            "token":self.token,
            }
        serializer = ActivateAccountSerializer(data = credentials)
        serializer.is_valid(raise_exception=True)
        credentials['user'] = self.user
        self.assertEqual(serializer.validated_data, credentials)
        with self.assertRaises(ValidationError) as context:
            serializer.save()
        self.assertEqual({"type":context.exception.detail["type"],"message":context.exception.detail["message"]},{"type":"account","message":"This account is already active. You can log in!"})
        serializer.validated_data["user"].is_active = False
        activated_user_account = serializer.save()
        self.assertTrue(activated_user_account.is_active)
    