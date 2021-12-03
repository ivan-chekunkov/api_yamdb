from rest_framework import serializers
from users.models import User
from rest_framework.validators import UniqueTogetherValidator
from reviews.models import Category, Genre, Title, Rewiev, Comment
from rest_framework.relations import SlugRelatedField




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


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)
    title = serializers.SlugRelatedField(slug_field='name', read_only=True)


    class Meta:
        fields = '__all__'
        model = Rewiev
        validators = [
            UniqueTogetherValidator(
                queryset=Rewiev.objects.all(),
                fields=('author', 'title'),
                message='Отзыв уже существует'

            )
        ]



class CodeSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True, max_length=150)

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment

