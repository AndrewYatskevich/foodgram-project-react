import pytest

from django.urls import reverse
from rest_framework import status

SHOPPING_URLS = {
    'get': 'api:recipes-download_shopping_cart',
    'create-delete': 'api:recipes-shopping_cart'
}


class TestShoppingView:

    @pytest.mark.django_db(transaction=True)
    def test_shopping_view_get(self, user_client_1, recipe, shopping_cart):
        try:
            response = user_client_1.get(reverse(SHOPPING_URLS.get('get')))
        except Exception as e:
            assert False, f'''Страница `/api/recipes/download_shopping_cart/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_200_OK, (
            'Неверный статус код запроса post `/api/recipes/download_shopping_cart/`'
        )

    def test_shopping_view_create(self, user_client_1, recipe):
        try:
            response = user_client_1.post(
                reverse(SHOPPING_URLS.get('create-delete'), kwargs={'pk': recipe.id})
            )
        except Exception as e:
            assert False, f'''Страница `/api/recipes/{recipe.id}/shopping_cart` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_201_CREATED, (
            'Неверный статус код запроса post `/api/recipes/recipe_id/shopping_cart`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_shopping_view_delete(self, user_client_1, recipe):
        try:
            response = user_client_1.delete(
                reverse(SHOPPING_URLS.get('create-delete'), kwargs={'pk': recipe.id})
            )
        except Exception as e:
            assert False, f'''Страница `/api/recipes/{recipe.id}/shopping_cart` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            'Неверный статус код запроса delete `/api/recipes/recipe_id/shopping_cart`'
        )
