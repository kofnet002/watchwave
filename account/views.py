from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def check_username_exists(request):
    if not request.data.get('username'):
        return Response({'error': 'Bad_request'}, status=status.HTTP_400_BAD_REQUEST)

    username = request.data.get('username')
    try:
        User.objects.get(username=username)
        return Response({'username_exists': True}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'username_exists': False}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):
    return Response({
        'detail': 'Welcome to the Watch~wave~',
        'endpoints':[{
            'get all vidoes - [GET]' : '/api/v1/vid/',
            'home - [GET]' : '/api/v1/home',
            'all users - [GET]' : '/api/v1/auth/users/',
            'register - [POST]' : '/api/v1/auth/users/',
            'activate acount - [POST]' : '/api/v1/auth/users/activation/',
            'login - [POST]' : '/api/v1/auth/jwt/create/',
            'login - [POST]' : '/auth/jwt/create/',
            'password reset request - [POST]' : '/api/v1/auth/users/reset_password/',
            'password reset request - [POST]' : '/api/v1/auth/users/reset_password_confirm/',
        }
        ]
        }, 
        status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.data.get('username'))
            if not user.is_active:
                return Response({'detail': 'Account not activated'}, status=status.HTTP_401_UNAUTHORIZED)
            if user.is_deactivated:
                return Response({'detail': 'Account deactivated'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'Invalid username or password'}, status=status.HTTP_400_BAD_REQUEST)

        return super().post(request, *args, **kwargs)