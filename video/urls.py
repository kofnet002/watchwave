from django.urls import path
from . import views


urlpatterns = [
    path('videos/', views.VideoView.as_view(), name='videos'),
    path('videos/<str:id>/', views.SingleVideo.as_view()),
]
