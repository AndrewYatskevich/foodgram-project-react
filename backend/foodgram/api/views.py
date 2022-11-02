import io

from django.conf import settings
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.rl_config import TTFSearchPath
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from recipes.models import Ingredient, Recipe, RecipeIngredient, Tag, User

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .serializers import (IngredientSerializer, RecipeSerializer,
                          TagSerializer, UserDetailsSerializer,
                          UserSubscriptionsSerializer)

TTFSearchPath.append(
    str(settings.BASE_DIR) + '/lib/reportlabs/fonts')


class UserViewSet(DjoserUserViewSet):
    pagination_class = LimitOffsetPagination

    def retrieve(self, request, *args, **kwargs):
        if 'me' in request.get_full_path():
            serializer = UserDetailsSerializer(request.user, context={
                'request': request})
            return Response(serializer.data, status=200)
        try:
            user = User.objects.get(pk=kwargs.get('pk'))
        except User.DoesNotExist:
            return Response(status=404)
        serializer = UserDetailsSerializer(user, context={
            'request': request})
        return Response(serializer.data, status=200)

    @action(methods=['get'], detail=False, url_path='subscriptions')
    def get_subscriptions(self, request):
        queryset = request.user.subscriptions.all()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSubscriptionsSerializer(page, many=True,
                                                     context={
                                                         'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = UserSubscriptionsSerializer(queryset, many=True,
                                                 context={'request': request})
        return Response(serializer.data, status=200)

    @action(methods=['post', 'delete'], detail=True, url_path='subscribe')
    def create_destroy_subscribe(self, request, pk=None):
        if request.method == 'POST':
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response(status=400)
            serializer = UserSubscriptionsSerializer(user, context={
                'request': request})
            request.user.subscriptions.add(user)
            return Response(serializer.data, status=201)
        try:
            user = request.user.subscriptions.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=400)
        serializer = UserSubscriptionsSerializer(user,
                                                 context={'request': request})
        request.user.subscriptions.remove(user)
        return Response(serializer.data, status=204)


class RecipeViewSet(viewsets.ModelViewSet):
    serializer_class = RecipeSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        request_user = self.request.user
        if 'is_favorited' in self.request.query_params:
            return request_user.favorite.all()
        if 'is_in_shopping_cart' in self.request.query_params:
            return request_user.shopping_cart.all()
        return Recipe.objects.all()

    def perform_create(self, serializer):
        tags_id = serializer.initial_data.get('tags')
        tags = Tag.objects.filter(id__in=tags_id)

        serializer.save(author=self.request.user, tags=tags)

    def perform_update(self, serializer):
        if 'tags' in self.request.data:
            tags_id = serializer.initial_data.get('tags')
            tags = Tag.objects.filter(id__in=tags_id)
            serializer.save(tags=tags)
        else:
            serializer.save()

    @action(methods=['get'], detail=False, url_path='download_shopping_cart')
    def download_shopping_cart(self, request):
        shopping_cart = {}
        recipes = request.user.shopping_cart.all()
        data = RecipeIngredient.objects.filter(recipe__in=recipes)
        for recipe_ingredient in data:
            ingredient_name = recipe_ingredient.ingredient.name
            measurement_unit = recipe_ingredient.ingredient.measurement_unit
            amount = recipe_ingredient.amount
            if ingredient_name in shopping_cart.keys():
                shopping_cart[ingredient_name][0] += amount
            else:
                shopping_cart[ingredient_name] = [amount, measurement_unit]

        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

        textob = c.beginText(40, 680)
        textob.setTextOrigin(inch, inch)
        pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))
        textob.setFont('FreeSans', 14)

        lines = []

        lines.append('Список покупок:')
        lines.append('')
        for ingredient_name, amount_data in shopping_cart.items():
            lines.append(
                f'{ingredient_name}: {amount_data[0]} {amount_data[1]}')

        for line in lines:
            textob.textLines(line)

        c.drawText(textob)
        c.showPage()
        c.save()
        buf.seek(0)

        return FileResponse(buf, as_attachment=True,
                            filename='shopping_cart.pdf')

    @action(methods=['post', 'delete'], detail=True, url_path='favorite')
    def create_destroy_favorite(self, request, pk=None):
        if request.method == 'POST':
            try:
                recipe = Recipe.objects.get(pk=pk)
            except Recipe.DoesNotExist:
                return Response(status=400)
            request.user.favorite.add(recipe)
            return Response(status=201)
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return Response(status=400)
        request.user.favorite.remove(recipe)
        return Response(status=204)

    @action(methods=['post', 'delete'], detail=True, url_path='shopping_cart')
    def create_destroy_shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            try:
                recipe = Recipe.objects.get(pk=pk)
            except Recipe.DoesNotExist:
                return Response(status=400)
            request.user.shopping_cart.add(recipe)
            return Response(status=201)
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return Response(status=400)
        request.user.shopping_cart.remove(recipe)
        return Response(status=204)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('^name',)
