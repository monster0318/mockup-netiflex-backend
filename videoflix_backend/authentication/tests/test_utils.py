from django.test import SimpleTestCase
from authentication.api.utils import message_body
from config.config_settings import *

class TestUtils(SimpleTestCase):

    def test_message_body(self):
        user_email = 'mario@gmail.com'
        reset_link = "https://videoflix.ibrahima-sourabie.com/account/reset-password/"

        subject,message,from_email,recipient_list = message_body(reset_link,user_email)
        self.assertIn(subject,"Videoflix Reset Password")
        self.assertEqual(from_email,MAIL_USERNAME)
        self.assertEqual(len(recipient_list), 2)
        self.assertIn(user_email,recipient_list)
        self.assertIn(MAIL_USERNAME,recipient_list)
        self.assertTemplateUsed("reset_password.html")