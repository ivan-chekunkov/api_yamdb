from users.models import User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .serializers import UserInfoSerializer, EmailSerializer, CodeSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from .permissions import AdminPermission, ModeratorPermission
from random import randint


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
