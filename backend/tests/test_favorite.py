import pytest


class TestFavoriteView:

    @pytest.mark.django_db(transaction=True)
    def test_favorite_view_create(self, user_client_1, recipe):
        try:
            response = user_client_1.post(f'/api/recipes/{recipe.id}/favorite/')
        except Exception as e:
            assert False, f'''Страница `/api/recipes/{recipe.id}/favorite` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == 201, (
            'Неверный статус код запроса post `/api/recipes/recipe_id/favorite`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_favorite_view_delete(self, user_client_1, recipe):
        try:
            response = user_client_1.delete(f'/api/recipes/{recipe.id}/favorite/')
        except Exception as e:
            assert False, f'''Страница `/api/recipes/{recipe.id}/favorite` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == 204, (
            'Неверный статус код запроса delete `/api/recipes/recipe_id/favorite`'
        )
