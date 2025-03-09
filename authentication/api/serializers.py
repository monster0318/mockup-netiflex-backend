from user.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes
from authentication.api.utils import message_body
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password

class UserAccountSerializer(serializers.ModelSerializer):
    """
    User account model serializer with first name and last name 
    added for enabling their view
    """
    class Meta:
        model = User
        fields = ['id','email','phone','address']

class LoginSerializer(serializers.Serializer):
    """
    User login serializer to enable secure form sent. Users can login
    with email and password.
    """

    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only = True)
    remember_me = serializers.BooleanField(default=False)


    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise serializers.ValidationError({"type":"email","message":"No user found with this email"})
        else:
            raise serializers.ValidationError({"type":"email","message":"Please provide an email, field is missing"})
        
        if not user.is_active:
            raise serializers.ValidationError({"type":"account","message":"User account is not activated"})
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError({"type":"credentials","message":"Wrong Email or password"})
        
        data['user'] = user
        return data

class RegisterSerializer(serializers.ModelSerializer):
    """"
    User registration serializer allowing user to register using their password
    and email. 
    """
    confirm_password = serializers.CharField(write_only = True)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ['email','password','confirm_password']
        extra_kwargs = {
            "password":{
                "write_only":True
            }
         
        }

    

    def validate(self, data):
        """ Validating user data """
        
        has_pwd_match = data.get("password") == data.get("confirm_password")
        entered_email = data.get('email', [])
        email_list = User.objects.filter(email=entered_email)

        if len(entered_email)==0:
            raise serializers.ValidationError({"type":"email","message":"Email address is required"})
       
        if len(email_list) > 0:
            raise serializers.ValidationError({"type":"email","message":"This Email already exists"})
        
        try:
            validate_password(data.get("password")) 
        except ValidationError as e:
            raise serializers.ValidationError({"type":"password","message":e.messages})
        
        if not has_pwd_match:
             raise serializers.ValidationError({"type":"password","message":"Passwords must match"})
        return data

    
    def save(self):
        """Saving user data if no error happened"""

        self.validated_data.pop('confirm_password')
        user = User(
            email=self.validated_data.get('email'),
        )
        user.set_password(self.validated_data.get('password'))
        user.is_active = False
        user.save()
        return user
    

class ActivateAccountSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, data):

        try:
            uid = urlsafe_base64_decode(data.get('uid')).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError):
            raise serializers.ValidationError({"type":"token","message":"Invalid user ID or token"})
        if not default_token_generator.check_token(user, data.get('token')):
            raise serializers.ValidationError({"type":"token","message":"Invalid or expired token"})
        
        data['user'] = user
        return data 

    def save(self):
        user = self.validated_data.get('user')
        if user.is_active:
            raise serializers.ValidationError({"type":"account","message":"This account is already active. You can log in!"})
        else:
            user.is_active = True
            user.save()
            return user

class ResetPasswordSerializer(serializers.Serializer):
    """ Reset user's password"""
    email = serializers.EmailField()

    def validate(self, data):
        entered_email = data.get('email')

        try:
            validate_email(entered_email)
        except ValidationError as e:
            raise serializers.ValidationError({"type":"email","message":e.messages})
        if not User.objects.filter(email=entered_email).exists():
            raise serializers.ValidationError({"type":"email","message":"No account found with this email"})
        return data

    def save(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f"http://localhost:4200/reset-password/{uid}/{token}/"

        subject,message,from_email,recipient_list = message_body(reset_link,email)
       
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

        has_pwd_match = data.get("new_password") == data.get("confirm_new_password")

        try:
            uid = urlsafe_base64_decode(data['uid']).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError):
            raise serializers.ValidationError({"type":"token","message":"Invalid user ID or token"})

        if not default_token_generator.check_token(user, data.get('token')):
            raise serializers.ValidationError({"type":"token","message":"Invalid or expired token"})
        
        if  not has_pwd_match:
             raise serializers.ValidationError({"type":"password","message":"Passwords must match"})
        
        data['user'] = user
        return data
       
    def save(self):
   
        self.validated_data.pop('confirm_new_password')
        user = self.validated_data['user']
        user.set_password(self.validated_data.get('new_password'))
        user.save()
        return user