from django.contrib import admin
from django.conf import settings

from .models import Recipe, RecipeIngredient, Tag, Ingredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
            'id',
            'author',
            'name',
            'image',
            'text',
            'get_tags',
            'cooking_time'
        )
    search_fields = ('name',)
    list_filter = ('name', 'author', 'tags')
    empty_value_display = settings.EMPTY_FIELD

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = settings.EMPTY_FIELD


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = settings.EMPTY_FIELD


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    search_fields = ('id',)
    list_filter = ('id',)
    empty_value_display = settings.EMPTY_FIELD
