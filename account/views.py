from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenObtainPairSerializer, UserSerializer
from drf_spectacular.utils import extend_schema




User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    # parser_classes = (MultiPartParser, FormParser, FileUploadParser,)
    @extend_schema(
            request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'email': {},
                    'password': {},
                    },
                'required': ['email', 'password'], 
                }
            },
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
            request={
            'multipart/form-data': {
                'type': 'object',
                'properties': {
                    'refresh': {},
                    },
                'required': ['refresh'], 
                }
            },
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
            return Response({'success': False, 'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # If the serializer is valid, perform token refresh
        refresh = serializer.validated_data
        return Response({'success': True, 'data': refresh}, status=status.HTTP_200_OK)



