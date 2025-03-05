from rest_framework.test import APITestCase
from fixtures.factories import UserFactory
from user.models import CustomUser



class TestUserModel(APITestCase):
    """Test cases for user model"""

    def setUp(self):
        self.user = UserFactory()


##############################################################################
###             TEST CASES FOR USER MODEL
##############################################################################


    def test_user_model(self):
        """Testing user model"""
        
        return_data = self.user.to_dict()
 
        self.assertEqual(len(CustomUser.objects.all()),1)
        self.assertIn("username",return_data)
        self.assertIn("email",return_data)
        self.assertIn("phone",return_data)
        self.assertIn("address",return_data)
