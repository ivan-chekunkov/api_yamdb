import uuid

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from api_yamdb.settings import ADMIN_EMAIL
from reviews.models import Category, Genre, Review, Title
from .filters import TitleFilter
from .mixins import CreateOrListViewSet
from .permissions import (AdminPermission, AuthorOrAdminOrModeratorReadOnly,
                          IsAdminOrReadOnly)
from .serializers import (CategorySerializer, CodeSerializer,
                          CommentSerializer, EmailSerializer, GenreSerializer,
                          ReviewSerializer, TitleSerializer,
                          TitleSerializerDeep, UserInfoSerializer,
                          UserSerializer)

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def send_code_confirmation(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']
    confirmation_code = uuid.uuid3(uuid.NAMESPACE_DNS, email)
    User.objects.create(
        username=username,
        email=email,
        confirmation_code=confirmation_code,
    )
    send_mail(
        'Токен доступа',
        f'Отправляем вам докен доступа: {confirmation_code}',
        ADMIN_EMAIL,
        [email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_user_token_auth(request):
    serializer = CodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = serializer.validated_data['confirmation_code']
    username = serializer.validated_data['username']
    user = get_object_or_404(User, username=username)
    if confirmation_code != user.confirmation_code:
        return Response(
            {'confirmation_code': 'Код подтверждения неверный'},
            status=status.HTTP_400_BAD_REQUEST
        )
    token = AccessToken.for_user(user)

    return Response({f'token: {token}'}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (AdminPermission,)
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = LimitOffsetPagination
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    def partial_update(self, request, *args, **kwargs):
        username = kwargs['username']
        user = get_object_or_404(User, username=username)
        serializer = UserSerializer(
            user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False, methods=['GET', 'PATCH'],
        url_path='me', url_name='me',
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        serializer = UserInfoSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UserInfoSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    filterset_class = TitleFilter
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['category', 'genre', 'year', 'name']
    permission_classes = (IsAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleSerializer
        return TitleSerializerDeep


class CategoryViewSet(CreateOrListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    permission_classes = (IsAdminOrReadOnly,)


class GenreViewSet(CreateOrListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrAdminOrModeratorReadOnly,)
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        new_queryset = title.reviews.all()
        return new_queryset


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrAdminOrModeratorReadOnly,)
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        query_comments = review.comments.all()
        return query_comments

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
