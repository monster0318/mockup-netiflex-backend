from django.http import Http404
from rest_framework.test import APITestCase
from user.models import User
from videoflix_app.models import Video
from fixtures.factories import VideoFactory,UserFactory
from videoflix_app.api.utils import get_or_404, seconds_to_time

class GetOr404Test(APITestCase):
    """Test get model or return 404 Not found"""
    
    def setUp(self):
        
        self.video = VideoFactory()
        self.user = UserFactory()
        
    def tearDown(self):
        Video.objects.all().delete()
        User.objects.all().delete()


    def test_get_model_from_pk(self):
        """Test get model for existing model and integer key"""

        model = get_or_404(User, self.user.pk)
        self.assertIsInstance(model,User)
        model = get_or_404(Video, str(self.video.pk))
        self.assertIsInstance(model,Video)


    def test_get_model_from_bad_pk(self):
        """Test get model for existing model and integer key"""

        with self.assertRaisesMessage(ValueError, "The ID must be an integer"):
            get_or_404(User, 'null')
        with self.assertRaisesMessage(Http404,"Model does not exist"):
            get_or_404(Video, 100)


    def test_seconds_to_time(self):
        """Test second conversion to time"""

        result = seconds_to_time(56)
        self.assertEqual(result,"00:56")
        result = seconds_to_time(120)
        self.assertEqual(result,"02:00")
        result = seconds_to_time(2*60*60)
        self.assertEqual(result,"02:00:00")