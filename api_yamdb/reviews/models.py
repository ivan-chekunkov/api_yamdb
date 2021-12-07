from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from users.models import User
from .validators import validate_year


class Category(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='URL slug'
    )

    class Meta:
        verbose_name = 'Категория',
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='URL slug'
    )

    class Meta:
        verbose_name = 'Жанр',
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование'
    )
    year = models.PositiveSmallIntegerField(
        validators=[validate_year],
        verbose_name='Год'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Произведение',
        verbose_name_plural = 'Произведения'


class Review(models.Model):
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата публикации'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name="reviews",
        blank=True,
        null=True,
        verbose_name='Произведение'
    )
    score = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1, message='Введите число не меньше 1'),
            MaxValueValidator(10, message='Введите число не больше 10')
        ],
        verbose_name='Рейтинг'
    )

    class Meta:
        verbose_name = 'Отзыв',
        verbose_name_plural = 'Отзывы',
        ordering = ['pub_date']
        constraints = [
            UniqueConstraint(
                fields=[
                    'author',
                    'title'],
                name='review')]

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        max_length=250,
        verbose_name='Текст комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Дата добавления'
    )

    class Meta:
        verbose_name = 'Комментарий',
        verbose_name_plural = 'Комментарии',

    def __str__(self):
        return self.text[:15]
