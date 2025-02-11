from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework import status
from django.contrib.auth import login
from rest_framework.response import Response
from authentication.api.serializers import ActivateAccountSerializer, ConfirmResetPasswordSerializer,\
      LoginSerializer, RegisterSerializer, ResetPasswordSerializer
from authentication.api.utils import guest_login, is_guest_user, is_guest_user_email


class Login(ObtainAuthToken):
    """Users can log in using their username and password
    
    Keyword arguments:
    argument -- username - username given during the registration
    Return: {username, email, token}
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        request_data = request.data
        
        if request_data and is_guest_user(request_data):
            log_data = guest_login(request=request)
        
            return Response(log_data, status=status.HTTP_200_OK)
        else:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                validated_user = serializer.validated_data['user']
                token, _ = Token.objects.get_or_create(user=validated_user)
                login(request,validated_user)

                user_data = {
                    "token":token.key,
                    "username":validated_user.username,
                    "email":validated_user.email,
                }
                return Response(user_data, status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
class GuestLogout(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        current_user = request.user 
        if is_guest_user_email(current_user.email):
            current_user.delete()
            return Response({"ok":True,"message":"Guest user successfully removed"}, status=status.HTTP_204_NO_CONTENT)
        return Response("",status=status.HTTP_400_BAD_REQUEST)
    
class Register(APIView):
    """Registration of new user"""

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data =request.data )
        
        if serializer.is_valid():
            saved_account = serializer.save()
            token, _ = Token.objects.get_or_create(user=saved_account)
            data={
                "token":token.key,
                "username":saved_account.username,
                "email":saved_account.email
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class ActivateAccountView(generics.CreateAPIView):
    """Activate user account after first sign up"""
    serializer_class = ActivateAccountSerializer
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = ActivateAccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Account successfully activated"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class ResetPasswordView(APIView):
    """
    This enable the user to send a request for resetting their 
    password when forgotten

    """
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self,request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Password reset link sent to your email!"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
class ResetPasswordConfirmView(APIView):
    """
    This enable the user to reset their 
    password when forgotten

    """
    serializer_class = ConfirmResetPasswordSerializer
    permission_classes = [AllowAny]
    
    def post(self,request):
        serializer = ConfirmResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Password successfully reset!"}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
