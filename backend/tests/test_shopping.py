import pytest


class TestShoppingView:

    @pytest.mark.django_db(transaction=True)
    def test_shopping_view_get(self, user_client_1, recipe, shopping_cart):
        try:
            response = user_client_1.get(f'/api/recipes/download_shopping_cart/')
        except Exception as e:
            assert False, f'''Страница `/api/recipes/download_shopping_cart/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == 200, (
            'Неверный статус код запроса post `/api/recipes/download_shopping_cart/`'
        )


    def test_shopping_view_create(self, user_client_1, recipe):
        try:
            response = user_client_1.post(f'/api/recipes/{recipe.id}/shopping_cart/')
        except Exception as e:
            assert False, f'''Страница `/api/recipes/{recipe.id}/shopping_cart` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == 201, (
            'Неверный статус код запроса post `/api/recipes/recipe_id/shopping_cart`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_shopping_view_delete(self, user_client_1, recipe):
        try:
            response = user_client_1.delete(f'/api/recipes/{recipe.id}/shopping_cart/')
        except Exception as e:
            assert False, f'''Страница `/api/recipes/{recipe.id}/shopping_cart` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == 204, (
            'Неверный статус код запроса delete `/api/recipes/recipe_id/shopping_cart`'
        )
