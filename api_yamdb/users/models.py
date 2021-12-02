from django.contrib.auth.models import AbstractUser
from django.db import models

CHOICES = (
    ('USER', 'Аутентифицированный пользователь'),
    ('MODERATOR', 'Модератор'),
    ('ADMIN', 'Администратор'),
    ('SUPERUSER', 'Суперюзер Django'),
)


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        blank=False,
    )
    role = models.CharField(
        max_length=35,
        choices=CHOICES,
        default='user',
        blank=False
    )
    confirmation_code = models.CharField(
        max_length=50,
        blank=True,
    )
    username = models.CharField(
        blank=False,
        unique=True,
        max_length=50,
    )
    bio = models.TextField(
        blank=True,
        max_length=500,
    )
