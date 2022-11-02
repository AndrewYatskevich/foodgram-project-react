from django_filters import rest_framework as filters
from recipes.models import Recipe


class RecipeFilter(filters.FilterSet):
    author = filters.CharFilter(
        field_name='author__id',
        lookup_expr='icontains',
    )
    tags = filters.CharFilter(method='filter_tags')

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def filter_tags(self, queryset, name, value):
        tags_params = self.request.query_params.getlist('tags')
        return queryset.filter(tags__slug__in=tags_params).distinct()
