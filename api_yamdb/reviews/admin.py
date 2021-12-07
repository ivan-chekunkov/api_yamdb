from django.contrib import admin

from .models import Category, Genre, Title


@admin.register(Genre)
class GenreInstanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Category)
class CategoryInstanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


@admin.register(Title)
class TitleInstanceAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'category',)
    list_filter = ('year', 'genre', 'category',)
