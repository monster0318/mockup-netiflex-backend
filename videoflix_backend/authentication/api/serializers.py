from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from authentication.api.utils import message_body


class UserAccountSerializer(serializers.ModelSerializer):
    """
    User account model serializer with first name and last name 
    added for enabling their view
    """
    class Meta:
        model = User
        fields = ['id','username','email']

class LoginSerializer(serializers.Serializer):
    """
    User login serializer to enable secure form sent. Users can login
    with email and password.
    """

    username = serializers.CharField(required = False)
    email = serializers.EmailField(required = False)
    password = serializers.CharField(write_only = True)
    remember_me = serializers.BooleanField(default=False)


    def validate(self, data):
   
        email = data.get("email",'')
        user_name = data.get('username', '')
        password = data["password"]

        if email:
            try:
                user = User.objects.get(email=email)
                username = user.username
            except User.DoesNotExist:
                raise serializers.ValidationError({"message":"No user found with this email."})
        elif user_name:
            username = user_name
        else:
            raise serializers.ValidationError({"message":"Please provide an email or a username, field is missing."})
        
        user = authenticate(username=username, password=password)
        if user is None:
            raise serializers.ValidationError({"message":"Incorrect email or password. Please try again."})
        elif not user.is_active:
            raise serializers.ValidationError({"message":"User account is disabled"})
        
        data['user'] = user
        return data

class RegisterSerializer(serializers.ModelSerializer):
    """"
    User registration serializer allowing user to register using their username, password
    and email. 
    """
    confirm_password = serializers.CharField(write_only = True)

    class Meta:
        model = User
        fields = ['username','email','password','confirm_password']
        extra_kwargs = {
            "password":{
                "write_only":True
            }
         
        }


    def validate(self, data):
        """ Validating user data """
        
        has_pwd_match = data["password"] == data["confirm_password"]
        entered_email = data['email']
        email_list = User.objects.filter(email=entered_email)

        if len(entered_email)==0:
            raise serializers.ValidationError({"message":"Email address is required"})
       
        if len(email_list) > 0:
            raise serializers.ValidationError({"message":"This Email already exists. Please chose a different email"})

        if  not has_pwd_match:
             raise serializers.ValidationError({"message":"Your passwords don't match. Try again"})
        return data

    
    def save(self):
        """Saving user data if no error happened"""

        self.validated_data.pop('confirm_password')
        user = User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            first_name=self.validated_data['username'],
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user
    


class ResetPasswordSerializer(serializers.Serializer):
    """ Reset user's password"""
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No account found with this email")
        return value

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"https://videoflix.ibrahima-sourabie.com/account/reset-password/{uid}/{token}/"

        subject,message,from_email,recipient_list = message_body(user.first_name,reset_link,email)
       
        email_to_send = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=recipient_list

        ) 
        email_to_send.content_subtype = "html"
        email_to_send.send()



class ConfirmResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate(self, data):

        has_pwd_match = data["new_password"] == data["confirm_new_password"]

        try:
            uid = urlsafe_base64_decode(data['uid']).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError):
            raise serializers.ValidationError("Invalid user ID or token.")

        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError("Invalid or expired token")
        
        if  not has_pwd_match:
             raise serializers.ValidationError({"message":"Passwords must match"})
        
        data['user'] = user
        return data
       

    def save(self):
   
        self.validated_data.pop('confirm_new_password')
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()