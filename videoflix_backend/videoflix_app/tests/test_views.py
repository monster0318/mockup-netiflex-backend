from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from user.models import CustomUser
from fixtures.factories import UserFactory, UserDataFactory, VideoDataFactory, VideoFactory
from videoflix_app.models import Video
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
 ###########################################################################################################################
 #####               TEST FOR ALL VIDEO VIEW
 ###########################################################################################################################

class VideoListTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.login_endpoint = reverse('login')
        cls.video_endpoint = reverse('video-list')
        cls.non_authorized_forbidden = [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    @classmethod
    def tearDownTestData(cls):
        print('I was call')
        Video.objects.all().delete()
        CustomUser.objects.all().delete()

    def setUp(self):
        self.user = UserFactory()
        self.video = VideoFactory(uploaded_by=self.user)
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION = "Token " + token.key)

    def tearDown(self):
        Video.objects.all().delete()
        CustomUser.objects.all().delete()

########################################################################
#          TEST CASES FOR VIDEO VIEW
#########################################################################

    def test_list_video_auth_user(self):
        """Test the retrieval of all videos for a authenticated user"""


        response = self.client.get(self.video_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        users = UserFactory.create_batch(5)
        for u in users:
            VideoFactory(uploaded_by=u)
        response = self.client.get(self.video_endpoint)
        self.assertEqual(len(response.data), 6)



    def test_list_video_non_auth_user(self):
        """Test the retrieval of all videos for a non authenticated user"""

        self.client.credentials()
        response = self.client.get(self.video_endpoint)
        self.assertIn(response.status_code, self.non_authorized_forbidden)
  

    def test_post_video_super_user(self):
        """Test the upload of video for a super user"""

        superuser_data = UserDataFactory()
        superuser = get_user_model().objects.create_superuser(**superuser_data.to_dict())
        video = VideoFactory(uploaded_by=superuser)        
        self.client.force_login(user=superuser)
        response = self.client.post(self.video_endpoint, video.to_dict(), format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.video_endpoint, {"fake":"video"}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_post_video_auth_user(self):
        """Test the upload of video for a authenticated user but not admin"""

        self.video_data = VideoDataFactory(uploaded_by=self.user)
        response = self.client.post(self.video_endpoint, self.video_data.to_dict(), format='multipart')
        self.assertIn(response.status_code, self.non_authorized_forbidden)


    def test_post_video_non_auth_user(self):
        """Test the upload of video for a non authenticated user"""

        self.video_data = VideoDataFactory(uploaded_by=self.user)
        response = self.client.post(self.video_endpoint, self.video_data.to_dict(), format='multipart')
        self.assertIn(response.status_code, self.non_authorized_forbidden)
 

#  ###########################################################################################################################
#  #####               TEST FOR SINGLE VIDEO VIEW
#  ###########################################################################################################################


class SingleVideoViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()
        cls.login_endpoint = reverse('login')
        cls.non_authorized_forbidden = [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN]

    @classmethod
    def tearDownTestData(cls):
        print('I was call')
        Video.objects.all().delete()
        CustomUser.objects.all().delete()

    def setUp(self):
        self.user = UserFactory()
        self.video = VideoFactory(uploaded_by=self.user)
        self.detail_video_endpoint = reverse('video-detail', kwargs={"pk":self.video.id})
        token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION = "Token " + token.key)
        
    def tearDown(self):
        Video.objects.all().delete()
        CustomUser.objects.all().delete()

# ########################################################################
# #          TEST CASES FOR SINGLE VIDEO VIEW
# #########################################################################


    def test_retrieve_single_video_auth_user(self):
        """Test the retrieval of single video for a authenticated user"""

        response = self.client.get(self.detail_video_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_single_video_non_auth_user(self):
        """Test the retrieval of single video for a non authenticated user"""

        self.client.credentials()
        response = self.client.get(self.detail_video_endpoint)
        self.assertIn(response.status_code, self.non_authorized_forbidden)
