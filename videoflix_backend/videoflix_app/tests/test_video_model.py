from rest_framework.test import APITestCase
from fixtures.factories import UserFactory, VideoFactory
from videoflix_app.models import Video



class TestUserModel(APITestCase):
    """Test case class for user model"""

    def setUp(self):
        self.video = VideoFactory()



##############################################################################
###             TEST CASES FOR USER MODEL
##############################################################################

    def test_string_representation(self):
        """Testing str representation of video instance"""
        
        self.assertEqual(str(self.video),self.video.title)


    def test_video_model_to_dict(self):
        """Testing video model"""

        return_data = self.video.to_dict()
        self.assertEqual(len(Video.objects.all()),1)
        self.assertEqual(return_data, {
            "title" :self.video.title,
            "description" :self.video.description,
            "category" :self.video.category,
            "uploaded_at" :self.video.uploaded_at,
            "updated_at" :self.video.updated_at,
            "created_by" :self.video.created_by,
            "is_favorite" :self.video.is_favorite,
            "language" :self.video.language,
            "video_file" :self.video.video_file,
        }
)