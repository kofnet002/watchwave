from django.urls import path, include
from . import views


urlpatterns = [
    path('exists', views.check_username_exists, name='exists'),
    path('home', views.home, name='home'),
]
