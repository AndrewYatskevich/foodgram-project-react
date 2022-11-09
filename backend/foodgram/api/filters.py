from django_filters.rest_framework import CharFilter, FilterSet

from recipes.models import Ingredient, Recipe


class RecipeFilter(FilterSet):
    author = CharFilter(
        field_name='author__id',
        lookup_expr='icontains',
    )
    tags = CharFilter(method='filter_tags')

    class Meta:
        model = Recipe
        fields = ('author', 'tags')

    def filter_tags(self, queryset, name, value):
        tags_params = self.request.query_params.getlist('tags')
        return queryset.filter(tags__slug__in=tags_params).distinct()


class IngredientFilter(FilterSet):
    name = CharFilter(
        field_name='name',
        lookup_expr='istartswith',
    )

    class Meta:
        model = Ingredient
        fields = ('name',)
