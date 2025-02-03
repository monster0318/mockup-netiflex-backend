from rest_framework import serializers

from user.models import CustomUser



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id','username','email','custom','phone','address']