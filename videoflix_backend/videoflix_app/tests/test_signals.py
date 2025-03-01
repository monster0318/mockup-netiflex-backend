from rest_framework.test import APITestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from fixtures.factories import UserFactory, VideoFactory
from videoflix_app.api.utils import VIDEO_EXTRA_FILES
from videoflix_app.models import Video
from unittest.mock import patch
from rest_framework.test import APIClient
import glob
import os



class TestSignals(APITestCase):
    """Testing signals"""

    def setUp(self):
        self.client = APIClient()
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

    @patch('videoflix_app.api.signals.update_video_file.si')
    @patch('videoflix_app.api.signals.create_vtt_file.si')
    @patch('videoflix_app.api.signals.convert_to_format.s')  
    def test_video_post_save(self, mock_convert_to_format,mock_create_vtt,mock_update_video):
        """Test the conversion of video after it is uploaded"""

        fake_video = SimpleUploadedFile("sample.mp4", b"fake_video_data", content_type="video/mp4")
        self.user = UserFactory()
        self.video = Video.objects.create(title="Test Video", description="Test Description", uploaded_by=self.user,video_file=fake_video)
        mock_convert_to_format.assert_called_once_with('media/videos/sample.mp4', ['hd360', 'hd480', 'hd720', 'hd1080'])
        mock_create_vtt.assert_called_once_with('media/videos/sample.mp4')
        mock_update_video.assert_called_once_with('media/videos/sample.mp4', 'videos/sample.mp4', VIDEO_EXTRA_FILES)



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
        mock_delete_files_starting_with.assert_called_once_with(source=original_file, file_suffixes=["_","-",""])