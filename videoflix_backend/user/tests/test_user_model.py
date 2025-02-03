from rest_framework.test import APITestCase
from fixtures.factories import UserFactory
from user.models import CustomUser



class TestUserModel(APITestCase):

    def setUp(self):
        self.user = UserFactory()



##############################################################################
###             TEST CASES FOR USER MODEL
##############################################################################


    def test_user_model(self):
        return_data = self.user.to_dict()

        self.assertEqual(len(CustomUser.objects.all()),1)
        self.assertEqual(return_data, {
            "username" : self.user.username,
            "email" : self.user.email,
            "custom" : self.user.custom,
            "phone" : self.user.phone,
            "address" : self.user.address
        }
)