import factory
import factory.fuzzy
from user.models import CustomUser
from videoflix_app.models import Video
from datetime import datetime
from django.core.files.uploadedfile import SimpleUploadedFile

class UserDataFactory(factory.Factory):

    id = factory.Sequence(lambda n:n+1)
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Sequence(lambda n: f"user{n}@videoflix.com")
    phone = factory.Faker("phone_number")
    address = factory.Faker("address")
    password = factory.PostGenerationMethodCall('set_password', 'FakePassword123!*')

    class Meta:
        model = CustomUser

class UserFactory(factory.django.DjangoModelFactory):

    id = factory.Sequence(lambda n:n+1)
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Faker("email")
    phone = factory.Faker("phone_number")
    address = factory.Faker("address")
    password = factory.PostGenerationMethodCall('set_password', 'FakePassword123!*')

    class Meta:
        model = CustomUser



class VideoDataFactory(factory.Factory):

    id = factory.Sequence(lambda n:n+1)
    title = factory.Faker("text", max_nb_chars=100)
    description = factory.Faker("text", max_nb_chars=1000)
    author = factory.Faker("name")
    genre = factory.fuzzy.FuzzyChoice(choices=["documentary","action","horror","drama","romance"])
    uploaded_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyAttribute(lambda obj: obj.uploaded_at)
    uploaded_by = factory.SubFactory(UserFactory)  
    is_favorite = factory.fuzzy.FuzzyChoice(choices=[True,False])
    language = factory.fuzzy.FuzzyChoice(choices=["french","english","german"])
    video_file = SimpleUploadedFile("test_video.mp4", b"fake_video_data", content_type="video/mp4")
    duration = factory.Faker("pyint", min_value=1,max_value=10)



    class Meta:
        model = Video

class VideoFactory(factory.django.DjangoModelFactory):

    id = factory.Sequence(lambda n:n+1)
    title = factory.Faker("text", max_nb_chars=100)
    description = factory.Faker("text", max_nb_chars=1000)
    author = factory.Faker("name")
    genre = factory.fuzzy.FuzzyChoice(choices=["documentary","action","horror","drama","romance"])
    uploaded_at = factory.LazyFunction(datetime.now)
    updated_at = factory.LazyAttribute(lambda obj: obj.uploaded_at)
    uploaded_by = factory.SubFactory(UserFactory)  
    is_favorite = factory.fuzzy.FuzzyChoice(choices=[True,False])
    language = factory.fuzzy.FuzzyChoice(choices=["french","english","german"])
    video_file = SimpleUploadedFile("test_video.mp4", b"fake_video_data", content_type="video/mp4")
    duration = factory.Faker("pyint", min_value=1,max_value=10)


    class Meta:
        model = Video