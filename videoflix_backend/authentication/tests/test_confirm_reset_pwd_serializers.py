from rest_framework.test import APITestCase, APIClient
from authentication.api.serializers import ConfirmResetPasswordSerializer
from user.models import CustomUser
from fixtures.factories import UserFactory
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes


class TestConfirmResetPasswordSerializer(APITestCase):
    """Testing Confirm reset password serializer"""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        

    def setUp(self):
        self.user = UserFactory()
        self.uid = urlsafe_base64_encode(force_bytes(self.user.id))
        self.token = default_token_generator.make_token(user = self.user) 
    
    def tearDown(self):
        CustomUser.objects.all().delete()



    def test_validate_confirm_reset_pwd_with_good_data(self):
        """Testing validate confirm reset password  with good data"""

        credentials = {
            "uid":self.uid,
            "token":self.token,
            "new_password":"Test456!",
            "confirm_new_password":"Test456!"
            }
        serializer = ConfirmResetPasswordSerializer(data = credentials)
        serializer.is_valid(raise_exception=True)
        credentials['user'] = self.user
        self.assertEqual(serializer.validated_data, credentials)
    
    def test_validate_confirm_reset_pwd_with_wrong_token(self):
        """Testing validate confirm reset password with wrong token"""

        user2 = UserFactory()
        self.token = default_token_generator.make_token(user = user2) 
        credentials = {
            "uid":self.uid,
            "token":self.token,
            "new_password":"Test456!",
            "confirm_new_password":"Test456!"
            }
        serializer = ConfirmResetPasswordSerializer(data = credentials)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEqual({"type":context.exception.detail["type"][0],"message":context.exception.detail["message"][0]},{"type":"token","message":"Invalid or expired token"})
    
    def test_validate_confirm_reset_pwd_of_non_existing_user(self):
        """Testing validate confirm reset password of non existing user"""

        self.uid = urlsafe_base64_encode(force_bytes(100))
        credentials = {
            "uid":self.uid,
            "token":self.token,
            "new_password":"Test456!",
            "confirm_new_password":"Test456!"
            }
        serializer = ConfirmResetPasswordSerializer(data = credentials)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEqual({"type":context.exception.detail["type"][0],"message":context.exception.detail["message"][0]},{"type":"token","message":"Invalid user ID or token"})
    
    def test_validate_confirm_reset_pwd_with_no_pwd_match(self):
        """Testing validate confirm reset password with not matching passwords"""

        credentials = {
            "uid":self.uid,
            "token":self.token,
            "new_password":"Test456!",
            "confirm_new_password":"TestFake456!"
            }
        serializer = ConfirmResetPasswordSerializer(data = credentials)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEqual({"type":context.exception.detail["type"][0],"message":context.exception.detail["message"][0]},{"type":"password","message":"Passwords must match"})
    
    def test_validate_save_new_pwd_with_good_data(self):
        """Testing validate reset password  with good data"""

        credentials = {
            "uid":self.uid,
            "token":self.token,
            "new_password":"Test456!",
            "confirm_new_password":"Test456!"
            }
        serializer = ConfirmResetPasswordSerializer(data = credentials)
        serializer.is_valid(raise_exception=True)
        credentials['user'] = self.user
        self.assertEqual(serializer.validated_data, credentials)
        old_password = 'FakePassword123!*'
        old_password_hash = self.user.password
        self.assertNotEqual(old_password, credentials.get('new_password'))
        saved_user = serializer.save()
        new_password = saved_user.password
        self.assertEqual(saved_user, self.user)
        self.assertNotEqual(new_password,old_password_hash)