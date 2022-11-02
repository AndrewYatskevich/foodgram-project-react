import pytest

from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user_1(django_user_model):
    user = django_user_model.objects.create_user(
        username='Test_User_1', password='1234567', email='user1@testmail.com'
    )
    return user


@pytest.fixture
def user_2(django_user_model):
    user = django_user_model.objects.create_user(
        username='Test_User_2', password='1234567', email='user2@testmail.com'
    )
    return user


@pytest.fixture
def user_client_1(user_1):
    token = Token.objects.create(user=user_1)
    client = APIClient(user_1)
    client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
    return client


@pytest.fixture
def user_1_subscribe(user_1, user_2):
    user_1.subscriptions.add(user_2)


@pytest.fixture
def user_1_favorite(user_1, recipe):
    user_1.favorite.add(recipe)
