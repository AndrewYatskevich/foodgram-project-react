import base64

from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer as DjoserCreateSerializer
from rest_framework import serializers

from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag, User


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

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Убедитесь, что значение не менее 1.')
        return value


class RecipeIngredientCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'amount')

    def validate_amount(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Убедитесь, что количество не менее 1.')
        return value

    def validate_ingredient(self, value):
        ingredients_id = [ingredient.get('ingredient') for ingredient in
                          self.initial_data]
        if len(ingredients_id) != len(set(ingredients_id)):
            raise serializers.ValidationError(
                'Убедитесь, что нет дублирующихся ингредиентов.')
        return value


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
        ingredients_data = []
        for ingredient in data:
            ingredients_data.append(
                {'ingredient': ingredient.get('id'),
                 'amount': ingredient.get('amount')}
            )
        return ingredients_data


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

    def validate_ingredients(self, value):
        serializer = RecipeIngredientCheckSerializer(data=value, many=True)
        serializer.is_valid(raise_exception=True)
        return value

    def validate_name(self, value):
        if len(value) > 200:
            raise serializers.ValidationError(
                'Длина названия не больше 200 символов')
        return value

    def validate_cooking_time(self, value):
        if value < 1:
            raise serializers.ValidationError(
                'Убедитесь, что значение не менее 1 мин.')
        return value

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)

        recipe_ingredient_data = []

        for ingredient_data in ingredients:
            ingredient_id = ingredient_data.get('ingredient')
            amount = ingredient_data.get('amount')
            recipe_ingredient_data.append(
                {'recipe': recipe.id, 'ingredient': ingredient_id,
                 'amount': amount}
            )

        serializer = RecipeIngredientCreateSerializer(
            data=recipe_ingredient_data, many=True
        )
        if not serializer.is_valid():
            raise serializers.ValidationError(serializer.errors)
        serializer.save()

        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        instance.tags.set(tags)

        if ingredients:
            recipe_ingredient_data = []

            for ingredient_data in ingredients:
                ingredient_id = ingredient_data.get('ingredient')
                amount = ingredient_data.get('amount')
                recipe_ingredient_data.append(
                    {'recipe': instance.id, 'ingredient': ingredient_id,
                     'amount': amount}
                )

            serializer = RecipeIngredientCreateSerializer(
                data=recipe_ingredient_data, many=True
            )
            if not serializer.is_valid():
                raise serializers.ValidationError(serializer.errors)
            RecipeIngredient.objects.filter(recipe=instance).delete()
            serializer.save()

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
