from rest_framework.test import APITestCase
from fixtures.factories import UserFactory, VideoFactory
from videoflix_app.models import Video



class TestUserModel(APITestCase):
    """Test case class for user model"""

    # def setUp(self):
    #     self.video = VideoFactory()



##############################################################################
###             TEST CASES FOR USER MODEL
##############################################################################


#     def test_video_model_to_dict(self):
#         return_data = self.video.to_dict()
#         self.assertEqual(len(Video.objects.all()),1)
#         self.assertEqual(return_data, {
#             "title" :self.title,
#             "description" :self.description,
#             "category" :self.category,
#             "uploaded_at" :self.uploaded_at,
#             "updated_at" :self.updated_at,
#             "created_by" :self.created_by,
#             "is_favorite" :self.is_favorite,
#             "language" :self.language,
#             "video_file" :self.video_file,
#         }
# )