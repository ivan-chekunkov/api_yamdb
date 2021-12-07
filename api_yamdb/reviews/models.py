from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from users.models import User

from .validators import validate_year

+
class Category(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='URL slug',
        unique=True
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='URL slug',
        unique=True
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Наименование',
        max_length=200
    )
    year = models.PositiveSmallIntegerField(
        verbose_name='Год',
        validators=[validate_year]
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        through_fields=('title', 'genre'),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='titles',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True
    )

+
class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )


class Review(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name="reviews", blank=True, null=True
    )
    +
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Рейтинг'
    )

    class Meta:
        +
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
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(max_length=250)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    def __str__(self):
        return self.text[:15]
