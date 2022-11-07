import pytest

from django.urls import reverse
from rest_framework import status

RECIPE_URLS = {
    'list': 'api:recipes-list',
    'detail': 'api:recipes-detail',
}


class TestRecipeView:

    @pytest.mark.django_db(transaction=True)
    def test_recipe_view_get(self, client, recipe, tag):
        try:
            response = client.get(reverse(RECIPE_URLS.get('list')))
        except Exception as e:
            assert False, f'''Страница `/api/recipes/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_200_OK, (
            'Неверный статус код запроса `/api/recipes/`')
        try:
            response = client.get(reverse(RECIPE_URLS.get('detail'), kwargs={'pk': recipe.id}))
        except Exception as e:
            assert False, f'''Страница `/api/recipes/<recipe_id>/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_200_OK, (
            'Неверный статус код запроса `/api/recipes/<recipe_id>/`')

    @pytest.mark.django_db(transaction=True)
    def test_recipe_view_create(self, mock_media, user_client_1, tag,
                                ingredient):
        TEST_RECIPE_DATA = {
            "ingredients": [
                {
                    "id": ingredient.id,
                    "amount": 10
                }
            ],
            "tags": [
                1
            ],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "string",
            "text": "string",
            "cooking_time": 1
        }

        try:
            response = user_client_1.post(
                reverse(RECIPE_URLS.get('list')),
                data=TEST_RECIPE_DATA,
                format="json"
            )
        except Exception as e:
            assert False, f'''Страница `/api/recipes/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_201_CREATED, (
            f'Неверный статус код запроса `/api/recipes/` {response.data}')

    @pytest.mark.django_db(transaction=True)
    def test_recipe_view_partial_update(self, mock_media, user_client_1,
                                        recipe, ingredient):
        TEST_RECIPE_DATA = {
            "ingredients": [
                {
                    "id": ingredient.id,
                    "amount": 5
                }
            ],
            "tags": [
                1
            ],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "stringP",
            "text": "stringPP",
            "cooking_time": 1
        }

        try:
            response = user_client_1.patch(
                reverse(RECIPE_URLS.get('detail'), kwargs={'pk': recipe.id}),
                data=TEST_RECIPE_DATA,
                format="json"
            )
        except Exception as e:
            assert False, f'''Страница `/api/recipes/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_200_OK, (
            f'Неверный статус код запроса `/api/recipes/` {response.data}')

    @pytest.mark.django_db(transaction=True)
    def test_recipe_view_delete(self, client, user_client_1, recipe):
        try:
            response = user_client_1.delete(reverse(RECIPE_URLS.get('detail'), kwargs={'pk': recipe.id}))
        except Exception as e:
            assert False, f'''Страница `/api/recipes/{recipe.id}/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_204_NO_CONTENT, (
            'Неверный статус код запроса delete `/api/recipes/recipe_id/`'
        )
