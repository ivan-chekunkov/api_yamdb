from rest_framework import serializers

from users.models import User
from rest_framework.validators import UniqueTogetherValidator


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    role = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class UserInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)   # maybe extra
    email = serializers.EmailField(required=True)   # maybe extra

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, max_length=150)
    username = serializers.CharField(required=True,)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Имя "me" запрещено.'
            )
        return value

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('email',),
                message='Эта электронная почта уже используется'
            ),
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('username',),
                message='Это имя пользователя уже используется'
            )
        ]


class CodeSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True, max_length=150)
