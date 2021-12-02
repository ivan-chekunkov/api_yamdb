from django.db import models

from .validators import validate_year


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
