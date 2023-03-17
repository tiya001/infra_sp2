import datetime as dt

from django.core.validators import MaxValueValidator, MinValueValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from users.validators import username_validator


User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    """Класс сериализатор категории."""

    class Meta:
        fields = ('name', 'slug',)
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Класс сериализатор жанра."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleListSerializer(serializers.ModelSerializer):
    """Класс сериализатор получения списка произведений."""

    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = ('id', 'name',
                            'year', 'description')


class CommentSerializer(serializers.ModelSerializer):
    """Сериалайзер комментариев."""

    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'pub_date', 'text')
        read_only_fields = ('id', 'pub_date')


class TitleCreateSerializer(serializers.ModelSerializer):
    """Класс сериализатор создания произведений."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        many=False,
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        required=False,
        queryset=Genre.objects.all()
    )

    class Meta:
        model = Title
        fields = '__all__'

    def year_validate(self, value):
        current_year = dt.date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего'
            )
        return value

    def to_representation(self, instance):
        return TitleListSerializer(instance, context=self.context).data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор модели User."""

    title = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True
    )
    score = serializers.IntegerField(
        validators=[
            MinValueValidator(1, 'Оценка должна быть не меньше 1.'),
            MaxValueValidator(10, 'Оценка должна быть не больше 10.')
        ],
    )

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        if self.context['request'].method == 'POST':
            title_id = self.context.get('view').kwargs.get('title_id')
            title = get_object_or_404(Title, id=title_id)
            request = self.context['request']
            author = request.user
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError('Вы уже оставили свой отзыв'
                                                  'к этому произведению!')
        return data


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        validators=(
            UnicodeUsernameValidator(),
        ),
        max_length=150
    )
    email = serializers.EmailField(
        max_length=254
    )

    def validate_username(self, username):
        if username.lower() == 'me':
            raise serializers.ValidationError('Недопустимое имя пользователя.')
        return username

    def validate(self, data):
        suspect_email = User.objects.filter(email=data['email']).exists()
        suspect_user = User.objects.filter(username=data['username']).exists()
        if User.objects.filter(username=data['username'],
                               email=data['email']).exists():
            return data
        if suspect_user:
            raise ValidationError('Это имя уже занято')
        if suspect_email:
            raise ValidationError('Эта почта уже зарегистрирована')
        return data

    class Meta:
        model = User
        fields = ('email',
                  'username',
                  )


class TokenSerializer(serializers.Serializer):
    confirmation_code = serializers.CharField(
        max_length=32,
    )
    username = serializers.CharField(max_length=150)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email',
                  'first_name', 'last_name', 'bio', 'role',)

    def validate_username(self, value):
        return username_validator(value)


class UserRestrictedSerializer(UserSerializer):
    username = serializers.CharField(
        max_length=150,
        required=True,
        validators=[
            username_validator,
        ]
    )
    email = serializers.EmailField(
        required=True,
        max_length=254
    )

    class Meta(UserSerializer.Meta):
        read_only_fields = ('username', 'email', 'role')
