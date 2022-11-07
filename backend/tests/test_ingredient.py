import pytest

from django.urls import reverse
from rest_framework import status

INGREDIENT_URLS = {
    'list': 'api:ingredients-list',
    'detail': 'api:ingredients-detail',
}


class TestIngredientView:

    @pytest.mark.django_db(transaction=True)
    def test_ingredient_view_get(self, client, ingredient):
        try:
            response = client.get(reverse(INGREDIENT_URLS.get('list')))
        except Exception as e:
            assert False, f'''Страница `/api/ingredients/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_200_OK, (
            'Неверный статус код запроса `/api/ingredients/`')
        try:
            response = client.get(reverse(INGREDIENT_URLS.get('detail'), kwargs={'pk': ingredient.id}))
        except Exception as e:
            assert False, f'''Страница `/api/ingredients/<ingredien_id>/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_200_OK, (
            'Неверный статус код запроса `/api/ingredients/<ingredien_id>/`')
