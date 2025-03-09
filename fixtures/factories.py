import factory
import factory.fuzzy
from user.models import User
from videoflix_app.models import Video
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile

class UserDataFactory(factory.Factory):

    id = factory.Sequence(lambda n:n+1)
    email = factory.Sequence(lambda n: f"user{n}@videoflix.com")
    phone = factory.Faker("phone_number")
    address = factory.Faker("address")
    password = factory.PostGenerationMethodCall('set_password', 'FakePassword123!*')

    class Meta:
        model = User

class UserFactory(factory.django.DjangoModelFactory):

    id = factory.Sequence(lambda n:n+1)
    email = factory.Faker("email")
    phone = factory.Faker("phone_number")
    address = factory.Faker("address")
    password = factory.PostGenerationMethodCall('set_password', 'FakePassword123!*')

    class Meta:
        model = User



class VideoDataFactory(factory.Factory):

    id = factory.Sequence(lambda n:n+1)
    title = factory.Faker("text", max_nb_chars=100)
    description = factory.Faker("text", max_nb_chars=1000)
    author = factory.Faker("name")
    genre = factory.fuzzy.FuzzyChoice(choices=["documentary","action","horror","drama","technic"])
    uploaded_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyAttribute(lambda obj: obj.uploaded_at)
    uploaded_by = factory.SubFactory(UserFactory)  
    is_favorite = factory.fuzzy.FuzzyChoice(choices=[True,False])
    language = factory.fuzzy.FuzzyChoice(choices=["french","english","german"])
    video_file = factory.LazyFunction(lambda: SimpleUploadedFile("test_video.mp4", b"fake_video_data"*1024, content_type="video/mp4"))
    poster = factory.Faker("text", max_nb_chars=200)
    vtt_file = factory.Faker("text", max_nb_chars=200)
    video_file_hd360 = factory.Faker("text", max_nb_chars=200)
    video_file_hd480 = factory.Faker("text", max_nb_chars=200)
    video_file_hd720 = factory.Faker("text", max_nb_chars=200)
    video_file_hd1080 = factory.Faker("text", max_nb_chars=200)
    duration = factory.Faker("pyint", min_value=1,max_value=100)



    class Meta:
        model = Video

class VideoFactory(factory.django.DjangoModelFactory):

    id = factory.Sequence(lambda n:n+1)
    title = factory.Faker("text", max_nb_chars=100)
    description = factory.Faker("text", max_nb_chars=1000)
    author = factory.Faker("name")
    genre = factory.fuzzy.FuzzyChoice(choices=["documentary","action","horror","drama","technic"])
    uploaded_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyAttribute(lambda obj: obj.uploaded_at)
    uploaded_by = factory.SubFactory(UserFactory)  
    is_favorite = factory.fuzzy.FuzzyChoice(choices=[True,False])
    language = factory.fuzzy.FuzzyChoice(choices=["french","english","german"])
    video_file = factory.LazyFunction(lambda: SimpleUploadedFile("test_video.mp4", b"fake_video_data"*1024, content_type="video/mp4"))
    poster = factory.Faker("text", max_nb_chars=200)
    vtt_file = factory.Faker("text", max_nb_chars=200)
    video_file_hd360 = factory.Faker("text", max_nb_chars=200)
    video_file_hd480 = factory.Faker("text", max_nb_chars=200)
    video_file_hd720 = factory.Faker("text", max_nb_chars=200)
    video_file_hd1080 = factory.Faker("text", max_nb_chars=200)
    duration = factory.Faker("pyint", min_value=1,max_value=100)


    class Meta:
        model = Video