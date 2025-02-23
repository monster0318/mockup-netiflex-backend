from rest_framework.test import APITestCase, APIClient
from authentication.api.serializers import LoginSerializer
from user.models import CustomUser
from fixtures.factories import UserFactory
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model


class TestLoginSerializer(APITestCase):
    """Testing login serializer"""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

    def setUp(self):
        self.user = UserFactory()
    
    def tearDown(self):
        CustomUser.objects.all().delete()



    def test_validate_login_good_data(self):
        """Testing validate login with good data"""

        login_data = {
            "email":self.user.email,
            "password":"FakePassword123!*",
            }
        serializer = LoginSerializer(data = login_data)
        serializer.is_valid(raise_exception=True)
        login_data['user'] = self.user
        login_data['remember_me'] = False
        self.assertEqual(serializer.validated_data, login_data)


    def test_validate_login_wrong_email(self):
        """Testing validate login with wrong email"""

        login_data = {
            "email":"testuser@gmail.com",
            "password":"Testuser123!",
            }
        serializer = LoginSerializer(data = login_data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)
        self.assertEqual({"type":context.exception.detail["type"][0],"message":context.exception.detail["message"][0]},{"type":"email","message":"No user found with this email"} )
    
    def test_validate_login_no_email_provided(self):
        """Testing validate login without email"""

        login_data = {
            "password":"Testuser123!",
            }
        serializer = LoginSerializer(data = login_data)
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertEqual({"type":context.exception.detail["type"][0],"message":context.exception.detail["message"][0]},{"type":"email","message":"Please provide an email or a username, field is missing"} )

    def test_authenticate_non_existing_user(self):
        """Testing authentication of non existing user"""

        serializer = LoginSerializer(data = {"email":self.user.email, "password":"password"})
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertEqual({"type":context.exception.detail["type"][0],"message":context.exception.detail["message"][0]},{"type":"credentials","message":"Wrong Email or password"})
    

    def test_authenticate_inactive_user(self):
        """Testing authentication of inactive user"""

        CustomUser.objects.all().delete()
        user = get_user_model().objects.create(username='test',email="testuser@gmail.com", password="password", is_active=False)
        serializer = LoginSerializer(data = {"email":user.email, "password":"password"})
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertEqual({"type":context.exception.detail["type"][0],"message":context.exception.detail["message"][0]},{"type":"account","message":"User account is not activated"})

        
