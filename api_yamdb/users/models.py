from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint


class UserRoles:
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    USER_ROLES = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )


class User(AbstractUser):

    email = models.EmailField(
        unique=True,
        blank=False,
        verbose_name='Электронная почта',
    )
    role = models.CharField(
        max_length=100,
        choices=UserRoles.USER_ROLES,
        default=UserRoles.USER,
        blank=False,
        verbose_name='Права доступа',
    )
    confirmation_code = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Код подтверждения',
    )
    username = models.CharField(
        blank=False,
        unique=True,
        max_length=150,
        verbose_name='Никнейм пользователя',
    )
    bio = models.TextField(
        blank=True,
        max_length=500,
        verbose_name='Биография',
    )
    first_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name='Имя',
    )
    last_name = models.CharField(
        blank=True,
        max_length=150,
        verbose_name='Фамилия',
    )

    class Meta:
        verbose_name = 'Пользователь',
        verbose_name_plural = 'Пользователи',
        constraints = [
            UniqueConstraint(fields=['email', ], name='email'),
            UniqueConstraint(fields=['username', ], name='username')
        ]

    @property
    def is_admin(self):
        return self.role == UserRoles.ADMIN

    @property
    def is_moderator(self):
        return self.role == UserRoles.MODERATOR

    @property
    def is_user(self):
        return self.role == UserRoles.USER
