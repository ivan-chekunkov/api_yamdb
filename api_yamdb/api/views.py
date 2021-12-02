from users.models import User
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import api_view, authentication_classes, action
from .serializers import UserInfoSerializer, EmailSerializer, CodeSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import uuid
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import AccessToken
from .permissions import AdminPermission


@api_view(['POST'])
# возможно убрать
def send_code_confirmation(request):
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data['email']
    username = serializer.data['username']
    if username == 'me':
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
    confirmation_code = uuid.uuid3(uuid.NAMESPACE_DNS, email)
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
@authentication_classes([])
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
    queryset = User.objects.all()
    #lookup_field = 'username'
    serializer_class = UserSerializer
    permission_classes = [AdminPermission]

    def perform_create(self, serializer):
        serializer.save(**serializer.validated_data)


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
