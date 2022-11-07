import pytest

from django.urls import reverse
from rest_framework import status

TAG_URLS = {
    'list': 'api:tags-list',
    'detail': 'api:tags-detail',
}


class TestTagView:

    @pytest.mark.django_db(transaction=True)
    def test_tag_view_get(self, client, tag):
        try:
            response = client.get(reverse(TAG_URLS.get('list')))
        except Exception as e:
            assert False, f'''Страница `/api/tags/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_200_OK, (
            'Неверный статус код запроса `/api/tags/`')
        try:
            response = client.get(
                reverse(TAG_URLS.get('detail'), kwargs={'pk': tag.id})
            )
        except Exception as e:
            assert False, f'''Страница `/api/tags/<tag_id>/` работает неправильно. Ошибка: `{e}`'''
        assert response.status_code == status.HTTP_200_OK, (
            'Неверный статус код запроса `/api/tags/<tag_id>/`')
