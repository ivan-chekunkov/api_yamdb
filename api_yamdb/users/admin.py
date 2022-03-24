from django.contrib import admin

from .models import User


@admin.register(User)
class GenreInstanceAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'first_name', 'last_name')
