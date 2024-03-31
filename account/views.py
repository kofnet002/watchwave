from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.parsers import MultiPartParser, FileUploadParser, FormParser

User = get_user_model()


# @api_view(['POST'])
# @permission_classes([AllowAny])
# @extend_schema(responses=UserSerializer)
# def check_username_exists(request):
#     if not request.data.get('username'):
#         return Response({'error': 'Bad_request'}, status=status.HTTP_400_BAD_REQUEST)

#     username = request.data.get('username')
#     try:
#         User.objects.get(username=username)
#         return Response({'username_exists': True}, status=status.HTTP_200_OK)

#     except User.DoesNotExist:
#         return Response({'username_exists': False}, status=status.HTTP_404_NOT_FOUND)


# @extend_schema(responses=UserSerializer)
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def home(request):
#     return Response({
#         'detail': 'Welcome to the Watch~wave~',
#         'endpoints':[{
#             'get all vidoes - [GET]' : '/api/v1/vid/',
#             'home - [GET]' : '/api/v1/home',
#             'all users - [GET]' : '/api/v1/auth/users/',
#             'register - [POST]' : '/api/v1/auth/users/',
#             'activate acount - [POST]' : '/api/v1/auth/users/activation/',
#             'login - [POST]' : '/api/v1/auth/jwt/create/',
#             'login - [POST]' : '/auth/jwt/create/',
#             'password reset request - [POST]' : '/api/v1/auth/users/reset_password/',
#             'password reset request - [POST]' : '/api/v1/auth/users/reset_password_confirm/',
#         }
#         ]
#         }, 
#         status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    # parser_classes = (MultiPartParser, FormParser, FileUploadParser,)
    @extend_schema(
            responses=UserSerializer,
            tags=['Auth'],
            summary='Log in user based on email and password and whether account is active  or deactivated',
            description='This endpoint checks if the user account is activated or deactivated',
            )
    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.data.get('email'))
            if not user.is_active:
                return Response({'detail': 'Account not activated'}, status=status.HTTP_401_UNAUTHORIZED)
            if user.is_deactivated:
                return Response({'detail': 'Account deactivated'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'success': False, 'detail': 'Wrong credentials'}, status=status.HTTP_400_BAD_REQUEST)

        return super().post(request, *args, **kwargs)


# Overwrite the TokenRefreshView to return custom response
class CustomTokenRefreshView(TokenRefreshView):
    # parser_classes = (MultiPartParser, FormParser, FileUploadParser)
    @extend_schema(
            responses=CustomTokenObtainPairSerializer,
            tags=['Auth'],
            summary='Token Refresh Endpoint',
            description='This endpoint refreshes the access token',
            )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            # If an exception occurs, return response with success=False
            return Response({'success': False, 'detail': str(e)}, status=400)

        # If the serializer is valid, perform token refresh
        refresh = serializer.validated_data
        return Response({'success': True, 'data': refresh}, status=200)