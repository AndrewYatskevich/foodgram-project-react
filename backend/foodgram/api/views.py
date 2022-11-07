from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from recipes.models import Ingredient, Recipe, Tag, User
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .pdf_generator import PdfGenerator
from .serializers import (IngredientSerializer, RecipeSerializer,
                          TagSerializer, UserDetailsSerializer,
                          UserSubscriptionsSerializer)


class UserViewSet(DjoserUserViewSet):
    pagination_class = CustomPagination

    def retrieve(self, request, *args, **kwargs):
        if 'me' in request.get_full_path():
            serializer = UserDetailsSerializer(request.user, context={
                'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        try:
            user = User.objects.get(pk=kwargs.get('pk'))
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserDetailsSerializer(user, context={
            'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='subscriptions',
            url_name='subscriptions')
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
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post', 'delete'], detail=True, url_path='subscribe',
            url_name='subscribe')
    def create_destroy_subscribe(self, request, pk=None):
        if request.method == 'POST':
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer = UserSubscriptionsSerializer(user, context={
                'request': request})
            request.user.subscriptions.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        try:
            user = request.user.subscriptions.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSubscriptionsSerializer(user,
                                                 context={'request': request})
        request.user.subscriptions.remove(user)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


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

    @action(methods=['get'], detail=False, url_path='download_shopping_cart',
            url_name='download_shopping_cart')
    def download_shopping_cart(self, request):
        pdf_file = PdfGenerator(request.user).generate()
        return FileResponse(pdf_file, as_attachment=True,
                            filename='shopping_cart.pdf')

    @action(methods=['post', 'delete'], detail=True, url_path='favorite',
            url_name='favorite')
    def create_destroy_favorite(self, request, pk=None):
        if request.method == 'POST':
            try:
                recipe = Recipe.objects.get(pk=pk)
            except Recipe.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            request.user.favorite.add(recipe)
            return Response(status=status.HTTP_201_CREATED)
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        request.user.favorite.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'delete'], detail=True, url_path='shopping_cart',
            url_name='shopping_cart')
    def create_destroy_shopping_cart(self, request, pk=None):
        if request.method == 'POST':
            try:
                recipe = Recipe.objects.get(pk=pk)
            except Recipe.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            request.user.shopping_cart.add(recipe)
            return Response(status=status.HTTP_201_CREATED)
        try:
            recipe = Recipe.objects.get(pk=pk)
        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        request.user.shopping_cart.remove(recipe)
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter
