from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.conf import settings

from django.contrib.auth import get_user_model

from users.models import Common

User = get_user_model()


class Category(Common):
    """Модель категорий."""

    class Meta(Common.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(Common):
    """Модель жанров."""

    class Meta(Common.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Модель заголовков."""

    name = models.CharField(
        'Название',
        max_length=100,
        db_index=True)
    year = models.PositiveSmallIntegerField(
        'Год',
        db_index=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle',
        blank=True,
        db_index=True
    )
    description = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель рецензии на произведение."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        db_column='title_id'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.SmallIntegerField(
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации обзора'
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'
        constraints = [
            models.UniqueConstraint(fields=['title_id', 'author'],
                                    name='unique_review')
        ]

    def __str__(self):
        return f'{self.text[settings.MA_NUM]}'


class Comment(models.Model):
    """Модель комментария к рецензии."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        db_column='review_id'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField('Дата комментария', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.text[settings.MA_NUM]}'


class GenreTitle(models.Model):
    genre_id = models.ForeignKey(Genre,
                                 on_delete=models.SET_NULL,
                                 null=True, verbose_name='Жанр',
                                 db_column='genre_id')
    title_id = models.ForeignKey(Title,
                                 on_delete=models.SET_NULL,
                                 null=True, verbose_name='Произведение',
                                 db_column='title_id')

    def __str__(self):
        return f'{self.genre_id} {self.title_id}'
