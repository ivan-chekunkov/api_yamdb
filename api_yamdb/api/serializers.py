from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        return User(**validated_data)

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'role', 'email',
        )


class UserInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)   # maybe extra
    email = serializers.EmailField(required=True)   # maybe extra

    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'role', 'email',
        )


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)


class CodeSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
