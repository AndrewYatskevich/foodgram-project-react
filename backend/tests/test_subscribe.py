import pytest


class TestSubscribeView:

    @pytest.mark.django_db(transaction=True)
    def test_subscriptions(self, user_client_1, user_1_subscribe):
        try:
            response = user_client_1.get(f'/api/users/subscriptions/?page=1&limit=6&recipes_limit=3')
        except Exception as e:
            assert False, f'''Страница `/api/users/subscriptions/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == 200, (
            'Неверный статус код запроса post `/api/users/subscriptions/`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_subscribe_view_create(self, user_client_1, user_2):
        try:
            response = user_client_1.post(f'/api/users/{user_2.id}/subscribe/')
        except Exception as e:
            assert False, f'''Страница `/api/users/{user_2.id}/subscribe` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == 201, (
            'Неверный статус код запроса post `/api/users/recipe_id/subscribe`'
        )

    @pytest.mark.django_db(transaction=True)
    def test_subscribe_view_delete(self, user_client_1, user_2, user_1_subscribe):
        try:
            response = user_client_1.delete(f'/api/users/{user_2.id}/subscribe/')
        except Exception as e:
            assert False, f'''Страница `/api/users/{user_2.id}/subscribe` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == 204, (
            'Неверный статус код запроса delete `/api/users/<user_id>/subscribe`'
        )
