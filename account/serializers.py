from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model
from djoser.serializers import PasswordResetConfirmSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

user = get_user_model()

# Add more fields when creating a new user
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 
                  'email',
                  'username', 
                  'password',
                  'is_active',
                  'is_admin',
                  'is_deactivated',
                ]


# Append the data below when user gets user details @ 'users/me/', 'users'
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 
                  'email',
                  'username',
                  'is_admin',
                  'is_active',
                  'is_deactivated',
                  'date_joined'
                  ]

    # this is where we send a request to slash me/ or auth/users
    def validate(self, attrs):
        validated_attr = super().validate(attrs)
        username = validated_attr.get('username')

        user = user.objects.get(username=username)

        if user.is_deactivated:
            raise ValidationError(
                'Account deactivated')

        if not user.is_active:
            raise ValidationError(
                'Account not activated')

# Add 'success' field for successful validation
        validated_attr['success'] = False

        return validated_attr


    def to_representation(self, instance):
            representation = super().to_representation(instance)
            return {'success': True, 'data': representation}

# Append the data below to the access & refresh tokens when user logs in
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        obj = self.user

        data.update({
            'id': obj.id, 
            'email': obj.email,
            'username': obj.username,
            'is_active': obj.is_active,
            'is_admin': obj.is_admin,
            'is_deactivated': obj.is_deactivated,
            'data_joined' : obj.date_joined,
        })
        
        response = {
            'success': True,
            'data': data
        }
        return response

class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    def save(self):
        # Call the parent's save method to perform the default behavior
        super().save()
        # Customize the response content
        return {
            "success": True,
            "message": "Password reset successful"
        }



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['is_admin'] = user.is_admin

        return token