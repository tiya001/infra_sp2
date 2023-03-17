from django.db import models

from django.contrib.auth.models import AbstractUser


USER_ROLES = [
    ('user', 'Пользователь'),
    ('moderator', 'Модератор'),
    ('admin', 'Админ'),
]


class User(AbstractUser):
    username = models.TextField(
        max_length=150,
        unique=True,
    )
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.TextField(max_length=150, blank=True)
    last_name = models.TextField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=100,
        choices=USER_ROLES,
        default='user'
    )
    confirmation_code = models.CharField(
        max_length=32,
        blank=True
    )

    @property
    def is_admin(self):
        return (self.role == 'admin'
                or self.is_superuser
                )

    @property
    def is_moderator(self):
        return self.role == 'moderator'


class Common(models.Model):
    name = models.TextField(
        verbose_name='Наименование',
        max_length=100
    )
    slug = models.SlugField(
        'slug',
        unique=True,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('name',)

    def __str__(self):
        return self.name
