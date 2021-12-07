from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import Category, Comment, Genre, Review, Title

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

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


class UserInfoSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    email = serializers.EmailField(read_only=True)
    role = serializers.CharField(read_only=True)

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


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id']
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ['id']
        model = Genre


class BaseTitleSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Title


class TitleSerializer(BaseTitleSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )


class TitleSerializerDeep(BaseTitleSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField(read_only=True)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)
    title = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        fields = '__all__'
        model = Review

    def validate(self, data):
        request = self.context['request']
        title_id = self.context.get('view').kwargs.get('title_id')
        user = request.user
        title = get_object_or_404(Title, pk=title_id)
        if (
            request.method == 'POST'
            and Review.objects.filter(title=title, author=user).exists()
        ):
            raise ValidationError('Отзыв уже существует')
        return data

    def validate_score(self, value):
        if 0 > value > 10:
            raise ValidationError('Оценка от 0 до 10')
        return value


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    review = serializers.SlugRelatedField(
        read_only=True, slug_field='text'
    )

    class Meta:
        fields = '__all__'
        model = Comment
