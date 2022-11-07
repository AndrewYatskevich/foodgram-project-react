import pytest

from django.urls import reverse
from rest_framework import status

USERS_URLS = {
    'list': 'api:users-list',
    'detail': 'api:users-detail',
    'set_password': 'api:users-set-password',
    'login': 'api:login',
    'logout': 'api:logout',
}

TEST_REGISTRATION_DATA = {
  "email": "vpupkin@yandex.ru",
  "username": "Test_User_3",
  "first_name": "Вася",
  "last_name": "Пупкин",
  "password": "Test_Pass_653"
}
TEST_PASSWORD_DATA = {
  "new_password": "Test_New_Pass_356",
  "current_password": "1234567"
}
TEST_LOGIN_DATA = {
  "password": "1234567",
  "email": "user2@testmail.com"
}


class TestUserView:

    @pytest.mark.django_db(transaction=True)
    def test_user_view_list(self, user_client_1, user_2):
        try:
            response = user_client_1.get(reverse(USERS_URLS.get('list')))
        except Exception as e:
            assert False, f'''Страница `/api/users/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_200_OK, (
            'Неверный статус код запроса `/api/users/`'
        )

    def test_user_view_retrieve(self, user_client_1, user_2, user_1_subscribe):
        try:
            response = user_client_1.get('/api/users/me/')
        except Exception as e:
            assert False, f'''Страница `/api/users/me/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_200_OK, (
            'Неверный статус код запроса `/api/users/me/`'
        )
        try:
            response = user_client_1.get(reverse(USERS_URLS.get('detail'), kwargs={'pk': user_2.id}))
        except Exception as e:
            assert False, f'''Страница `/api/users/<user_id>/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_200_OK, (
            'Неверный статус код запроса `/api/users/<user_id>/`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_user_view_registration(self, client, user_client_1, user_2):
        try:
            response = client.post(reverse(USERS_URLS.get('list')), data=TEST_REGISTRATION_DATA)
        except Exception as e:
            assert False, f'''Страница `/api/users/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_201_CREATED, (
            f'Неверный статус код запроса `/api/users/`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_user_view_set_password(self, client, user_client_1, user_2):
        try:
            response = user_client_1.post(reverse(USERS_URLS.get('set_password')), data=TEST_PASSWORD_DATA)
        except Exception as e:
            assert False, f'''Страница `/api/users/set_password/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            f'Неверный статус код запроса `/api/users/set_password/`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_user_login(self, client, user_2):
        try:
            response = client.post(reverse(USERS_URLS.get('login')), data=TEST_LOGIN_DATA)
        except Exception as e:
            assert False, f'''Страница `/api/auth/token/login/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_200_OK, (
            f'Неверный статус код запроса `/api/auth/token/login/`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_user_logout(self, user_client_1):
        try:
            response = user_client_1.post(reverse(USERS_URLS.get('logout')))
        except Exception as e:
            assert False, f'''Страница `/api/auth/token/logout/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            f'Неверный статус код запроса `/api/auth/token/logout/`'
        )
