import pytest

from django.urls import reverse
from rest_framework import status

SUBSCRIBE_URLS = {
    'list': 'api:users-subscriptions',
    'create-delete': 'api:users-subscribe'
}


class TestSubscribeView:

    @pytest.mark.django_db(transaction=True)
    def test_subscriptions(self, user_client_1, user_1_subscribe):
        try:
            response = user_client_1.get(reverse(SUBSCRIBE_URLS.get('list')))
        except Exception as e:
            assert False, f'''Страница `/api/users/subscriptions/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_200_OK, (
            'Неверный статус код запроса post `/api/users/subscriptions/`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_subscribe_view_create(self, user_client_1, user_2):
        try:
            response = user_client_1.post(
                reverse(SUBSCRIBE_URLS.get('create-delete'), kwargs={'pk': user_2.id})
            )
        except Exception as e:
            assert False, f'''Страница `/api/users/{user_2.id}/subscribe` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_201_CREATED, (
            'Неверный статус код запроса post `/api/users/recipe_id/subscribe`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_subscribe_view_delete(self, user_client_1, user_2, user_1_subscribe):
        try:
            response = user_client_1.delete(
                reverse(SUBSCRIBE_URLS.get('create-delete'), kwargs={'pk': user_2.id})
            )
        except Exception as e:
            assert False, f'''Страница `/api/users/{user_2.id}/subscribe` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            'Неверный статус код запроса delete `/api/users/<user_id>/subscribe`'
        )
