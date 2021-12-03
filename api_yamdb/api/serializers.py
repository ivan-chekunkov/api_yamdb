from rest_framework import serializers
from reviews.models import Category, Genre, Title, Rewiev, Comment
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


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



class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
