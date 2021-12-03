from rest_framework import filters, mixins, viewsets
from rest_framework.viewsets import ModelViewSet
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleSerializerDeep,
    ReviewSerializer,
    CommentSerializer)
from .filters import TitleFilter
from reviews.models import Category, Genre, Title, Rewiev
from .permissions import IsAuthorOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from django.shortcuts import get_object_or_404



class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    filterset_class = TitleFilter
    filterset_fields = ['category', 'genre', 'year', 'name']

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleSerializer
        return TitleSerializerDeep


class CategoryViewSet(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class GenreViewSet(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.CreateModelMixin,
                   mixins.DestroyModelMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
    
    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        rewiev = get_object_or_404(Rewiev, pk=self.kwargs.get('rewiev_id'))
        query_comments = rewiev.comments.all()
        return query_comments

    def perform_create(self, serializer):
        rewiev = get_object_or_404(Rewiev, pk=self.kwargs.get('rewiev_id'))
        serializer.save(author=self.request.user, rewiev=rewiev)
