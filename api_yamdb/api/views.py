from random import randint

from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import User

from .filters import TitleFilter
from .permissions import (AdminPermission, IsAuthorOrReadOnly,
                          ModeratorPermission)
from .serializers import (CategorySerializer, CodeSerializer,
                          CommentSerializer, EmailSerializer, GenreSerializer,
                          ReviewSerializer, TitleSerializer,
                          TitleSerializerDeep, UserInfoSerializer,
                          UserSerializer)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_code_confirmation(request):
    serializer = EmailSerializer(data=request.data)
    if not serializer.is_valid(raise_exception=True):
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    email = serializer.data['email']
    username = serializer.data['username']
    if username == 'me':
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    confirmation_code = randint(10000, 99999)
    user, created = User.objects.get_or_create(
        username=username,
        email=email,
        confirmation_code=confirmation_code,
    )
    if not created:
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    send_mail(
        'Токен доступа',
        f'Отправляем вам докен доступа: {confirmation_code}',
        'admin@admin.ru',
        [email],
        fail_silently=False,
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_user_token_auth(request):
    serializer = CodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = serializer.data['confirmation_code']
    username = serializer.data['username']
    user = get_object_or_404(User, username=username)
    if confirmation_code != user.confirmation_code:
        return Response(
            {'confirmation_code': 'Код подтверждения неверный'},
            status=status.HTTP_400_BAD_REQUEST
        )
    token = AccessToken.for_user(user)

    return Response({f'token: {token}'}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [AdminPermission, ]
    serializer_class = UserSerializer
    lookup_field = 'username'

    def get_queryset(self):
        return User.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=self.kwargs['username'])
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def perform_create(self, serializer):
        return super().perform_create(serializer)

    def perform_update(self, serializer):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=self.kwargs['username'])
        if user != self.request.user.username:
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=self.kwargs['username'])
        if user.is_superuser:
            return Response(instance.data, status=status.HTTP_403_FORBIDDEN)
        return super().perform_destroy(instance)


class UserInfo(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = User.objects.all(username=request.user.username)
        serializer = UserInfoSerializer(user)
        return Response(serializer._data, status=status.HTTP_200_OK)

    def patch(self, request):
        user = User.objects.all(username=request.user.username)
        serializer = UserInfoSerializer(user, data=request.data, partial=True)
        if serializer.is_valid:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


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
        rewiev = get_object_or_404(Review, pk=self.kwargs.get('rewiev_id'))
        query_comments = rewiev.comments.all()
        return query_comments

    def perform_create(self, serializer):
        rewiev = get_object_or_404(Review, pk=self.kwargs.get('rewiev_id'))
        serializer.save(author=self.request.user, rewiev=rewiev)
