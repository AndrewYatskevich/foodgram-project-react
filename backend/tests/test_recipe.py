import pytest
import json


class TestRecipeView:

    @pytest.mark.django_db(transaction=True)
    def test_recipe_view_get(self, client, recipe, tag):
        try:
            response = client.get(
                '/api/recipes/')
        except Exception as e:
            assert False, f'''Страница `/api/recipes/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == 200, (
            'Неверный статус код запроса `/api/recipes/`')
        try:
            response = client.get(f'/api/recipes/{recipe.id}/')
        except Exception as e:
            assert False, f'''Страница `/api/recipes/<recipe_id>/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == 200, (
            'Неверный статус код запроса `/api/recipes/<recipe_id>/`')

    @pytest.mark.django_db(transaction=True)
    def test_recipe_view_get_favorited(self, user_client_1, user_1_favorite,
                                       recipe):
        try:
            response = user_client_1.get('/api/recipes/')
        except Exception as e:
            assert False, f'''Страница `/api/recipes/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == 200, (
            'Неверный статус код запроса `/api/recipes/`')

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
            response = user_client_1.post('/api/recipes/', data=TEST_RECIPE_DATA, format="json")
        except Exception as e:
            assert False, f'''Страница `/api/recipes/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == 201, (
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
            response = user_client_1.patch(f'/api/recipes/{recipe.id}/',
                                           data=TEST_RECIPE_DATA, format="json")
        except Exception as e:
            assert False, f'''Страница `/api/recipes/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == 200, (
            f'Неверный статус код запроса `/api/recipes/` {response.data}')

    @pytest.mark.django_db(transaction=True)
    def test_recipe_view_delete(self, client, user_client_1, recipe):
        try:
            response = user_client_1.delete(f'/api/recipes/{recipe.id}/')
        except Exception as e:
            assert False, f'''Страница `/api/recipes/{recipe.id}/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == 204, (
            'Неверный статус код запроса delete `/api/recipes/recipe_id/`'
        )
        try:
            response = client.delete(f'/api/recipes/{recipe.id}/')
        except Exception as e:
            assert False, f'''Страница `/api/recipes/{recipe.id}/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == 401, (
            f'Неверный статус код запроса delete `/api/recipes/recipe_id/` {response.data}'
        )
