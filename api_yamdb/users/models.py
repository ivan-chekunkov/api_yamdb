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
    )
    role = models.CharField(
        max_length=100,
        choices=UserRoles.USER_ROLES,
        default=UserRoles.USER,
        blank=False,
    )
    confirmation_code = models.CharField(
        max_length=50,
        blank=True,
    )
    username = models.CharField(
        blank=False,
        unique=True,
        max_length=150,
    )
    bio = models.TextField(
        blank=True,
        max_length=500,
    )
    first_name = models.CharField(
        blank=True,
        max_length=150,
    )
    last_name = models.CharField(
        blank=True,
        max_length=150,
    )

    class Meta:
        constraints = [
            UniqueConstraint(fields=['email', ], name='email'),
            UniqueConstraint(fields=['username', ], name='username')
        ]
