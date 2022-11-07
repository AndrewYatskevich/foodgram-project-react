import pytest

from django.urls import reverse
from rest_framework import status

FAVORITE_URLS = {
    'create-delete': 'api:recipes-favorite'
}


class TestFavoriteView:

    @pytest.mark.django_db(transaction=True)
    def test_favorite_view_create(self, user_client_1, recipe):
        try:
            response = user_client_1.post(
                reverse(FAVORITE_URLS.get('create-delete'), kwargs={'pk': recipe.id})
            )
        except Exception as e:
            assert False, f'''Страница `/api/recipes/{recipe.id}/favorite` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_201_CREATED, (
            'Неверный статус код запроса post `/api/recipes/recipe_id/favorite`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_favorite_view_delete(self, user_client_1, recipe):
        try:
            response = user_client_1.delete(
                reverse(FAVORITE_URLS.get('create-delete'), kwargs={'pk': recipe.id})
            )
        except Exception as e:
            assert False, f'''Страница `/api/recipes/{recipe.id}/favorite` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            'Неверный статус код запроса delete `/api/recipes/recipe_id/favorite`'
        )
