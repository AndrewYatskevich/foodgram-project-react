import json

from recipes.models import Ingredient


def run():
    with open('data/ingredients.json', 'r',
              encoding='utf-8') as ingredients:
        data = json.load(ingredients)

        Ingredient.objects.bulk_create([
            Ingredient(
                name=ingredient.get('name'),
                measurement_unit=ingredient.get('measurement_unit'),
            ) for ingredient in data
        ])
