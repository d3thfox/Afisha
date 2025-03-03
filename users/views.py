
from users.serailizers import RegisterSerializer, AuthSerializer, ConfirmUserSerializer
from users.models import UserProfile
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
import random
 

from rest_framework.generics import ListCreateAPIView

class RegisterAPIView(ListCreateAPIView):

    def post(self, request, *args, **kwargs):

        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        confirmation_code = str(random.randint(100000, 999999))  

        user = User.objects.create_user(username=username, password=password, is_active=False)
        user_profile = UserProfile.objects.create(user=user, confirmation_code=confirmation_code)

        return Response(
            data={'user_id': user.id, 'confirmation_code': confirmation_code},
            status=status.HTTP_201_CREATED
        )



class LoginAPIView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:      

            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'token': token.key}, status=status.HTTP_200_OK)

        return Response(data={'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


        
class LoginAPIView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = AuthSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:      

            token, _ = Token.objects.get_or_create(user=user)
            return Response(data={'token': token.key}, status=status.HTTP_200_OK)

        return Response(data={'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)



class ConfirmRegisterAPIView(ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        serializer = ConfirmUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.confirm_user()

        return Response(
            data={'user_id': user.id, 'message': 'User successfully confirmed!'},
            status=status.HTTP_200_OK
        )





   

