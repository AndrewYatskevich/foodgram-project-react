import pytest


class TestIngredientView:

    @pytest.mark.django_db(transaction=True)
    def test_ingredient_view_get(self, client, ingredient):
        try:
            response = client.get('/api/ingredients/')
        except Exception as e:
            assert False, f'''Страница `/api/ingredients/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == 200, (
            'Неверный статус код запроса `/api/ingredients/`')
        try:
            response = client.get(f'/api/ingredients/{ingredient.id}/')
        except Exception as e:
            assert False, f'''Страница `/api/ingredients/<ingredien_id>/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == 200, (
            'Неверный статус код запроса `/api/ingredients/<ingredien_id>/`')
