from rest_framework.test import APITestCase, APIClient
from authentication.api.serializers import RegisterSerializer
from user.models import User
from fixtures.factories import UserFactory
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


class TestRegisterSerializer(APITestCase):
    """Testing registration serializer"""
    
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

    def setUp(self):
        self.user = UserFactory()
    
    def tearDown(self):
        User.objects.all().delete()

################# TEST CASES ################################################

    def test_validate_register_with_good_data(self):
        """Testing validate registration with good data"""

        register_data = {
            "email":"testuser@gmail.com",
            "password":"Testuser123!",
            "confirm_password":"Testuser123!"
            }
        serializer = RegisterSerializer(data = register_data)
        serializer.is_valid(raise_exception=True)
        self.assertEqual(serializer.validated_data, register_data)

    def test_validate_register_without_email(self):
        """Testing validate registration without email address"""

        register_data = {
            "username":"test",
            "password":"Testuser123!",
            "confirm_password":"Testuser123!"
            }
        serializer = RegisterSerializer(data = register_data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEqual({"type":context.exception.detail["type"][0],"message":context.exception.detail["message"][0]},{"type":"email","message":"Email address is required"})
    
    def test_validate_register_password_do_not_match(self):
        """Testing validate registration with passwords which do not match"""

        register_data = {
            "email":"testuser@gmail.com",
            "password":"Testuser789!",
            "confirm_password":"Testuser123!"
            }
        serializer = RegisterSerializer(data = register_data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEqual({"type":context.exception.detail["type"][0],"message":context.exception.detail["message"][0]},{"type":"password","message":"Passwords must match"} )

    def test_validate_register_existing_user_email(self):
        """Testing registration of user with existing email address"""

        register_data_user = {
            "email":self.user.email,
            "password":"Testuser1123!",
            "confirm_password":"Testuser1123!"
            }

        serializer = RegisterSerializer(data = register_data_user)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertEqual({"type":context.exception.detail["type"][0],"message":context.exception.detail["message"][0]},{"type":"email","message":"This Email already exists"})
    

    def test_validate_bad_password(self):
        """Testing register with bad password"""

        pwd_error = {"This password is too common.","This password is too short. It must contain at least 8 characters.","This password is entirely numeric."}

        serializer = RegisterSerializer(data = { "email":'test1@gmail.com',"password":"Test", "confirm_password":"Test"})
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(context.exception.detail["type"][0],"password")
        is_valid_error = set(context.exception.detail["message"]).issubset(pwd_error)
        self.assertTrue(is_valid_error)

        serializer = RegisterSerializer(data = { "email":'test2@gmail.com',"password":"112311111111", "confirm_password":"112311111111"})
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEqual(context.exception.detail["type"][0],"password")
        is_valid_error = set(context.exception.detail["message"]).issubset(pwd_error)
        self.assertTrue(is_valid_error)

        
    def test_save_registered_data(self):
        """Testing save data by registering"""

        register_data = {
            "email":"testuser@gmail.com",
            "password":"Testuser123!",
            "confirm_password":"Testuser123!"
            }
        User.objects.all().delete()
        serializer = RegisterSerializer(data = register_data)
        serializer.is_valid(raise_exception=True)
        self.assertEqual(serializer.validated_data, register_data)
        saved_user = serializer.save()
        self.assertEqual(User.objects.all().count(), 1)
        self.assertFalse(saved_user.is_active)
        self.assertIsInstance(saved_user, User)
