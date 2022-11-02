import tempfile
import pytest

from recipes.models import Recipe, Tag, Ingredient, RecipeIngredient


@pytest.fixture()
def mock_media(settings):
    with tempfile.TemporaryDirectory() as temp_directory:
        settings.MEDIA_ROOT = temp_directory
        yield temp_directory


@pytest.fixture
def tag():
    return Tag.objects.create(
        name='TestTagName',
        color='TestTagColor',
        slug='TestTagSlug',
    )


@pytest.fixture
def ingredient():
    return Ingredient.objects.create(
        name='TestIngredientName',
        measurement_unit='TestUnit',
    )


@pytest.fixture
def ingredient_2():
    return Ingredient.objects.create(
        name='TestIngredientName2',
        measurement_unit='TestUnit2',
    )


@pytest.fixture
def recipe(user_1, tag, ingredient):
    recipe = Recipe.objects.create(
        author=user_1,
        name='TestRecipe',
        text='TestText',
        cooking_time=1
    )
    recipe.tags.add(tag)
    RecipeIngredient.objects.create(
        recipe=recipe,
        ingredient=ingredient,
        amount=5
    )
    return recipe


@pytest.fixture
def shopping_cart(user_1, recipe):
    user_1.shopping_cart.add(recipe)
