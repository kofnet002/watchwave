import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user():
    def _create_user(email, username, password, is_active=True, is_deactivated=False):
        user = User.objects.create_user(
            email=email,
            username=username,
            password=password,
        )
        user.is_active = is_active
        user.is_deactivated = is_deactivated
        user.save()
        return user
    return _create_user

@pytest.fixture
def user_data():
    return {
        'email': 'testuser@example.com',
        'username': 'testuser',
        'password': 'testpassword123'
    }

@pytest.mark.django_db
def test_user_creation(api_client, user_data):
    url = reverse('user_create')
    response = api_client.post(url, user_data, format='json')
    assert response.status_code == 201
    assert 'id' in response.data

@pytest.mark.django_db
def test_user_login(api_client, create_user, user_data):
    create_user(**user_data)
    url = reverse('custom_jwt_create')
    response = api_client.post(url, {'email': user_data['email'], 'password': user_data['password']}, format='json')
    assert response.status_code == 200
    assert 'access' in response.data['data']
    assert response.data['success'] is True

@pytest.mark.django_db
def test_user_login_wrong_credentials(api_client, create_user, user_data):
    create_user(**user_data)
    url = reverse('custom_jwt_create')
    response = api_client.post(url, {'email': user_data['email'], 'password': 'wrongpassword'}, format='json')
    assert response.status_code == 401
    # assert response.data['success'] is False

@pytest.mark.django_db
def test_token_refresh(api_client, create_user, user_data):
    user = create_user(**user_data)
    refresh = RefreshToken.for_user(user)
    url = reverse('token_refresh')
    response = api_client.post(url, {'refresh': str(refresh)}, format='json')
    assert response.status_code == 200
    assert 'access' in response.data['data']
    assert response.data['success'] is True

@pytest.mark.django_db
def test_user_details(api_client, create_user, user_data):
    user = create_user(**user_data)
    refresh = RefreshToken.for_user(user)
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    url = reverse('user')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data['success'] is True
    assert response.data['data']['email'] == user_data['email']
    assert response.data['data']['username'] == user_data['username']
