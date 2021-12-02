from rest_framework import serializers

from reviews.models import Category, Genre, Title


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
