from rest_framework.test import APITestCase, APIClient
from authentication.api.serializers import LoginSerializer
from user.models import CustomUser
from fixtures.factories import UserFactory
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

class TestLoginSerializer(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = UserFactory()
    
    def tearDown(self):
        CustomUser.objects.all().delete()



    def test_validate_login_good_data(self):
        """Testing validate login with good data"""

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

    def test_authenticate_none_existing_user(self):
        """Testing authentication of non existing user"""

        serializer = LoginSerializer(data = {"email":self.user.email, "password":"password"})
        with self.assertRaises(ValidationError) as context:
            serializer.is_valid(raise_exception=True)

        self.assertEqual({"type":context.exception.detail["type"][0],"message":context.exception.detail["message"][0]},{"type":"credentials","message":"Wrong Email or password"})

        
        