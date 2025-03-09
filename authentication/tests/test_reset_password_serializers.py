from rest_framework.test import APITestCase, APIClient
from authentication.api.serializers import ResetPasswordSerializer
from user.models import User
from fixtures.factories import UserFactory
from rest_framework.exceptions import ValidationError
from unittest.mock import patch
from authentication.api.utils import message_body

class TestResetPasswordSerializer(APITestCase):
    """Testing reset password serializer"""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

    def setUp(self):
        self.user = UserFactory()
    
    def tearDown(self):
        User.objects.all().delete()



    def test_validate_reset_pwd_good_data(self):
        """Testing validate reset password with good data"""

        email_address = {
            "email":self.user.email,
            }
        serializer = ResetPasswordSerializer(data = email_address)
        serializer.is_valid(raise_exception=True)
        self.assertEqual(serializer.validated_data, email_address)


    def test_validate_reset_password_no_account_email(self):
        """Testing validate reset password with with no account email"""

        email_address = {
            "email":"testuser@gmail.com",
            }
        serializer = ResetPasswordSerializer(data = email_address)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEqual({"type":context.exception.detail["type"][0],"message":context.exception.detail["message"][0]},{"type":"email","message":"No account found with this email"})
    
    def test_validate_reset_password_invalid_email(self):
        """Testing validate reset password with with wrong email"""

        invalid_email_address = {
            "email":"testusüüergmail",
            }
        serializer = ResetPasswordSerializer(data = invalid_email_address)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(context.exception.detail["email"][0],"Enter a valid email address.")
    
    @patch("authentication.api.serializers.EmailMessage")
    def test_save_reset_pwd_good_data(self, email_msg_mock):
        """Testing function EmailMessage() when saving reset password"""

        email_address = {
            "email":self.user.email,
            }
        serializer = ResetPasswordSerializer(data = email_address)
        serializer.is_valid(raise_exception=True)
        self.assertEqual(serializer.validated_data, email_address)
        serializer.save()
        email_msg_mock.assert_called_once()
    
    @patch("authentication.api.serializers.message_body")
    def test_save_reset_pwd_good_data_message_body_call(self, msg_body_mock):
        """Testing function message_body() call when saving reset password"""

        email_address = {
            "email":self.user.email,
            }
        serializer = ResetPasswordSerializer(data = email_address)
        serializer.is_valid(raise_exception=True)
        self.assertEqual(serializer.validated_data, email_address)
        msg_body_mock.return_value = ("Videoflix Reset Password", 
                                      "Hi you requested ....",
                                      "test@gmail.com",
                                      ["testmail@gmail.com"])
        serializer.save()
        msg_body_mock.assert_called_once()
    

