import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from account.models import User
from video.models import Video

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def admin_user(db):  # Using the 'db' fixture to allow database access
    return User.objects.create_user(email='admin@test.com', username='admin', password='adminpass', is_admin=True)

@pytest.fixture
def normal_user(db):  # Using the 'db' fixture to allow database access
    return User.objects.create_user(email='user@test.com', username='user', password='userpass')

@pytest.fixture
def video(admin_user, db):  # Using the 'db' fixture to allow database access
    return Video.objects.create(
        user=admin_user,
        title="Test Video",
        description="Test Description",
        video_url="http://test.com/video.mp4"
    )

@pytest.mark.django_db  # Marking the test with django_db to allow database access
def test_get_all_videos(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('videos')
    response = api_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_upload_video_as_admin(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    url = reverse('videos')
    data = {
        'title': 'New Video',
        'description': 'New Description',
        'video': open('testing.mp4', 'rb')
    }
    response = api_client.post(url, data, format='multipart')
#     assert response.status_code == 201

@pytest.mark.django_db
def test_upload_video_as_normal_user(api_client, normal_user):
    api_client.force_authenticate(user=normal_user)
    url = reverse('videos')
    data = {
        'title': 'New Video',
        'description': 'New Description',
        'video': open('testing.mp4', 'rb')
    }
    response = api_client.post(url, data, format='multipart')
    assert response.status_code == 403

@pytest.mark.django_db
def test_get_single_video(api_client, admin_user, video):
    api_client.force_authenticate(user=admin_user)
    url = reverse('single-video', kwargs={'id': video.id})
    response = api_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_update_video_as_admin(api_client, admin_user, video):
    api_client.force_authenticate(user=admin_user)
    url = reverse('single-video', kwargs={'id': video.id})
    data = {'title': 'Updated Title', 'description': 'Updated Description'}
    response = api_client.put(url, data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_update_video_as_normal_user(api_client, normal_user, video):
    api_client.force_authenticate(user=normal_user)
    url = reverse('single-video', kwargs={'id': video.id})
    data = {'title': 'Updated Title', 'description': 'Updated Description'}
    response = api_client.put(url, data)
    assert response.status_code == 403

@pytest.mark.django_db
def test_delete_video_as_admin(api_client, admin_user, video):
    api_client.force_authenticate(user=admin_user)
    url = reverse('single-video', kwargs={'id': video.id})
    response = api_client.delete(url)
    assert response.status_code == 204

@pytest.mark.django_db
def test_delete_video_as_normal_user(api_client, normal_user, video):
    api_client.force_authenticate(user=normal_user)
    url = reverse('single-video', kwargs={'id': video.id})
    response = api_client.delete(url)
    assert response.status_code == 403

@pytest.mark.django_db
def test_get_next_video(api_client, admin_user, video):
    api_client.force_authenticate(user=admin_user)
    url = reverse('next-video-api', kwargs={'current_video_id': video.id})
    response = api_client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_get_previous_video(api_client, admin_user, video):
    api_client.force_authenticate(user=admin_user)
    url = reverse('previous-video-api', kwargs={'current_video_id': video.id})
    response = api_client.get(url)
    assert response.status_code == 200
