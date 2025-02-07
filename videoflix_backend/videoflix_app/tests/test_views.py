from rest_framework.test import APITestCase
from django.urls import reverse
from django.test import Client
from rest_framework import status
from user.models import CustomUser
from fixtures.factories import UserFactory, UserDataFactory, VideoDataFactory, VideoFactory
from videoflix_app.models import Video
from django.contrib.auth import get_user_model

 ###########################################################################################################################
 #####               TEST FOR ALL VIDEO VIEW
 ###########################################################################################################################

class VideoListTest(APITestCase):

    def setUp(self):
        self.client = Client()
        self.login_endpoint = reverse('login')
        self.video_endpoint = reverse('video-list')



    def tearDown(self):
        Video.objects.all().delete()
        CustomUser.objects.all().delete()



########################################################################
#          TEST CASES FOR VIDEO VIEW
#########################################################################

    def test_list_video_auth_user(self):
        """Test the retrieval of all videos for a authenticated user"""

        self.user = UserFactory()
        self.video = VideoFactory()
        self.client.post(self.login_endpoint, {"email":self.user.email, "password":"FakePassword123!*"},format='json')
        response = self.client.get(self.video_endpoint)
        print('VIDEO',self.video.to_dict())
        print('CONTENT',response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        # self.assertEqual(response.data[0], self.video.to_dict()) # serializer for author
        for _ in range(5):
            self.video_tmp = VideoFactory()
        self.assertEqual(len(response.data), 6)



    def test_list_video_non_auth_user(self):
        """Test the retrieval of all videos for a non authenticated user"""

        self.user = UserFactory()
        self.video = VideoFactory()
        response = self.client.get(self.video_endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"ok":False,"message":"You don't have the permission for this operation"})

    def test_post_video_super_user(self):
        """Test the upload of video for a super user"""
        superuser_data = UserDataFactory()
        self.user = get_user_model().objects.create_superuser(**superuser_data.to_dict())        
        self.video_data = { "title": "Test Video",
                           "author":"Mario",
                            "description": "This is a test video",
                            "created_by":self.user,
                            "category": "action",
                            "language": "english"
                        }
       
        self.client.force_login(user=self.user)
        with open("media/video_test/test_video.mp4", 'rb') as video:
            self.video_data["video_file"] = video
            response = self.client.post(self.video_endpoint, self.video_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.video_endpoint, {"fake":"video"}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_post_video_auth_user(self):
        """Test the upload of video for a authenticated user but not admin"""

        self.user = UserFactory()
        self.video_data = VideoDataFactory()
        self.client.post(self.login_endpoint, {"email":self.user.email, "password":"FakePassword123!*"},format='json')
        response = self.client.post(self.video_endpoint, self.video_data.to_dict(), format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"ok":False,"message":"You don't have the permission for this operation"})


    def test_post_video_non_auth_user(self):
        """Test the upload of video for a non authenticated user"""

        self.user = UserFactory()
        self.video_data = VideoDataFactory()
        response = self.client.post(self.video_endpoint, self.video_data.to_dict(), format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"ok":False,"message":"You don't have the permission for this operation"})
 

 ###########################################################################################################################
 #####               TEST FOR SINGLE VIDEO VIEW
 ###########################################################################################################################


class SingleVideoViewTest(APITestCase):

    def setUp(self):
        self.client = Client()
        self.login_endpoint = reverse('login')
        



    def tearDown(self):
        Video.objects.all().delete()
        CustomUser.objects.all().delete()

########################################################################
#          TEST CASES FOR SINGLE VIDEO VIEW
#########################################################################


    def test_retrieve_single_video_auth_user(self):
        """Test the retrieval of single video for a authenticated user"""
        self.video = VideoFactory()
        self.detail_video_endpoint = reverse('video-detail', kwargs={"pk":self.video.id})

        self.user = UserFactory()
        self.client.post(self.login_endpoint, {"email":self.user.email, "password":"FakePassword123!*"},format='json')
        response = self.client.get(self.detail_video_endpoint)
        print('FIRST',response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data, self.video.to_dict())

    def test_retrieve_single_video_non_auth_user(self):
        """Test the retrieval of single video for a non authenticated user"""
        self.video = VideoFactory()
        self.detail_video_endpoint = reverse('video-detail', kwargs={"pk":self.video.id})

        self.user = UserFactory()
        response = self.client.get(self.detail_video_endpoint)
        print('SECOND',response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, {"ok":False,"message":"You don't have the permission for this operation"})