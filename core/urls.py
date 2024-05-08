"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from djoser.views import UserViewSet
from account.views import CustomTokenObtainPairView
from account.views import CustomTokenRefreshView
from decouple import config
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = config('ADMIN_SITE_HEADER')
admin.site.index_title = "Admin"


urlpatterns = [
    path('admin/', admin.site.urls),

    # path('api/v1/auth/', include('djoser.urls')),
    # path('api/v1/auth/', include('djoser.urls.jwt')),

    # CUSTOMIZED DJOSER URLS, EXTRACTED THE NEEDES ONES
    path('api/v1/auth/user/activate/', UserViewSet.as_view({"post": "activation"}), name='activate'),
    path('api/v1/auth/users/', UserViewSet.as_view({"get": "list"}), name='users'),
    path('api/v1/auth/users/me/', UserViewSet.as_view({"get": "me"}), name='user'),
    path('api/v1/auth/reset-password/', UserViewSet.as_view({"post": "reset_password"}), name='reset_password'),
    path('api/v1/auth/reset-password-confirm/', UserViewSet.as_view({"post": "reset_password_confirm"}), name='reset_password_confirm'),

    path('api/v1/', include('account.urls')),
    path('api/v1/', include('video.urls')),
    path('auth/jwt/create/', CustomTokenObtainPairView.as_view(), name='custom_jwt_create'),
    path('auth/jwt/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    path('apischema/', SpectacularAPIView.as_view(), name='schema'),
    path('', SpectacularSwaggerView.as_view(url_name='schema')),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
