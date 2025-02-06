from rest_framework.test import APITestCase
from django.test import Client
from videoflix_app.models import Video
from unittest.mock import patch
from fixtures.factories import UserFactory, VideoFactory
import os
from django.db.models.signals import post_save, post_delete
import glob
from django.core.files.uploadedfile import SimpleUploadedFile



class TestSignals(APITestCase):

    def setUp(self):
        self.client = Client()
        Video.objects.all().delete()
        list_file = glob.glob("media/videos/test_video*")
        if list_file:
            for file in list_file:
                os.remove(file)



    def tearDown(self):
        Video.objects.all().delete()
        list_file = glob.glob("media/videos/test_video*")
        if list_file:
            for file in list_file:
                os.remove(file)



########################################################################
#          TEST CASES FOR SIGNALS
#########################################################################

    @patch("videoflix_app.api.signals.convert_to_format")
    def test_video_post_save(self, convert_to_format):
        """Test the conversion of video after it is uploaded"""

        fake_video = SimpleUploadedFile("sample.mp4", b"fake_video_data", content_type="video/mp4")
        self.user = UserFactory()
        self.video = Video.objects.create(title="Test Video", description="Test Description", created_by=self.user,video_file=fake_video)
        convert_to_format.assert_called_with(source="media/videos/sample.mp4",quality='hd1080')
        self.assertEqual(convert_to_format.call_count, 4)


    @patch("videoflix_app.api.signals.delete_files_starting_with") 
    def test_delete_video_on_file_delete(self, mock_delete_files_starting_with):
        """Test the deletion of video from folder when file is deleted"""
        
        self.video = VideoFactory()

        self.video_url = self.video.video_file.name
        expected_url = "videos/test_video.mp4"
        self.assertEqual(self.video_url, expected_url)

        self.video.delete()
        original_file = self.video.video_file.name
        original_file = os.path.join("media/", original_file)

        mock_delete_files_starting_with.assert_called_with(source=original_file, file_postfix="")
        self.assertEqual(mock_delete_files_starting_with.call_count, 3)