import base64

from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer as DjoserCreateSerializer
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag, User
from rest_framework import serializers


class UserCreateSerializer(DjoserCreateSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class UserDetailsSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(default=False)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed')

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user
        if request_user.is_authenticated:
            if obj in request_user.subscriptions.all():
                return True
        return False


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit', 'amount')

    def get_amount(self, obj):
        recipe = self.context.get('recipe')
        return RecipeIngredient.objects.get(recipe=recipe,
                                            ingredient=obj).amount


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ('recipe', 'ingredient', 'amount')

    def create(self, validated_data):
        pass

    def get_amount(self, obj):
        recipe = self.context.get('recipe')
        return RecipeIngredient.objects.get(recipe=recipe,
                                            ingredient=obj).amount


class Image(serializers.ImageField):

    def to_internal_value(self, data):
        format, imgstr = data.split(';base64,')
        ext = format.split('/')[-1]
        return ContentFile(base64.b64decode(imgstr), name='temp.' + ext)


class RecipeIngredientField(serializers.FileField):
    def to_representation(self, value):
        recipe = value.instance
        serializer = RecipeIngredientSerializer(
            value, read_only=True,
            many=True,
            context={'recipe': recipe}
        )
        return serializer.data

    def to_internal_value(self, data):
        return {}


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(read_only=True, many=True)
    author = UserDetailsSerializer(read_only=True)
    ingredients = RecipeIngredientField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    image = Image()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_ingredients(self, obj):
        ingredients = obj.ingredients.all()
        serializer = RecipeIngredientSerializer(ingredients, read_only=True,
                                                many=True,
                                                context={'recipe': obj})
        return serializer.data

    def create(self, validated_data):
        validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        ingredients = self.initial_data.get('ingredients')

        for ingredient_data in ingredients:
            ingredient_id = ingredient_data.get('id')
            ingredient = Ingredient.objects.get(id=ingredient_id)
            amount = ingredient_data.get('amount')
            RecipeIngredient.objects.create(recipe=recipe,
                                            ingredient=ingredient,
                                            amount=amount)

        return recipe

    def update(self, instance, validated_data):
        validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.tags.set(tags)

        if 'ingredients' in self.initial_data:
            ingredients = self.initial_data.get('ingredients')
            RecipeIngredient.objects.filter(recipe=instance).delete()

            for ingredient_data in ingredients:
                ingredient_id = ingredient_data.get('id')
                ingredient = Ingredient.objects.get(id=ingredient_id)
                amount = ingredient_data.get('amount')
                RecipeIngredient.objects.create(recipe=instance,
                                                ingredient=ingredient,
                                                amount=amount)

        return instance

    def get_is_favorited(self, obj):
        request_user = self.context.get('request').user
        if request_user.is_authenticated:
            if obj in request_user.favorite.all():
                return True
        return False

    def get_is_in_shopping_cart(self, obj):
        request_user = self.context.get('request').user
        if request_user.is_authenticated:
            if obj in request_user.shopping_cart.all():
                return True
        return False


class RecipeSubscriptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class UserSubscriptionsSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(default=False)
    recipes = RecipeSubscriptionsSerializer(read_only=True, many=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    @staticmethod
    def get_recipes_count(obj):
        return obj.recipes.all().count()

    def get_is_subscribed(self, obj):
        request_user = self.context.get('request').user
        if request_user.is_authenticated:
            if obj in request_user.subscriptions.all():
                return True
        return False
