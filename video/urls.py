from django.urls import path
from . import views
# from uuid import UUID


urlpatterns = [
    path('videos/', views.VideoView.as_view(), name='videos'),
    path('videos/<str:id>/', views.SingleVideo.as_view(), name='single-video'),
    path('next-video/<uuid:current_video_id>/', views.NextVideoAPIView.as_view(), name='next-video-api'),
    path('previous-video/<uuid:current_video_id>/', views.PreviousVideoAPIView.as_view(), name='previous-video-api'),
]

