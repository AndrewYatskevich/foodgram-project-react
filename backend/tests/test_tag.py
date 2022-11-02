import pytest


class TestTagView:

    @pytest.mark.django_db(transaction=True)
    def test_tag_view_get(self, client, tag):
        try:
            response = client.get('/api/tags/')
        except Exception as e:
            assert False, f'''Страница `/api/tags/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == 200, (
            'Неверный статус код запроса `/api/tags/`')
        try:
            response = client.get(f'/api/tags/{tag.id}/')
        except Exception as e:
            assert False, f'''Страница `/api/tags/<tag_id>/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == 200, (
            'Неверный статус код запроса `/api/tags/<tag_id>/`')
