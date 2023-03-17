from django.contrib import admin

from import_export import resources
from import_export.admin import ImportExportModelAdmin

from users.models import User
from reviews.models import Genre, Category, Title, Review, Comment, GenreTitle





class UserResource(resources.ModelResource):

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'role',
            'bio',
            'first_name',
            'last_name',
        )


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    resource_classes = [UserResource]
    list_display = (
        'id',
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
    )


class GenreResource(resources.ModelResource):

    class Meta:
        model = Genre
        fields = (
            'id',
            'name',
            'slug',
        )


class CategoryResource(resources.ModelResource):

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
        )


class TitleResource(resources.ModelResource):

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'genre',
            'description',
            'category',
        )


class ReviewResource(resources.ModelResource):

    class Meta:
        model = Review
        fields = (
            'id',
            'title',
            'score',
            'text',
            'author',
            'pub_date',
        )


class CommentResource(resources.ModelResource):

    class Meta:
        model = Comment
        fields = (
            'id',
            'review',
            'text',
            'author',
            'pub_date',
        )


class GenreTitleResource(resources.ModelResource):

    class Meta:
        model = GenreTitle
        fields = (
            'id',
            'genre_id',
            'title_id',
        )


@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = [CategoryResource]
    list_display = (
        'id',
        'name',
        'slug',
    )


@admin.register(Genre)
class GenreAdmin(ImportExportModelAdmin):
    resource_classes = [GenreResource]
    list_display = (
        'id',
        'name',
        'slug',
    )


@admin.register(Title)
class TitleAdmin(ImportExportModelAdmin):
    resource_classes = [TitleResource]
    list_display = (
        'id',
        'name',
        'year',
        'description',
        'category',
    )


@admin.register(Review)
class ReviewAdmin(ImportExportModelAdmin):
    resource_classes = [ReviewResource]
    list_display = (
        'id',
        'title',
        'score',
        'text',
        'author',
        'pub_date',
    )


@admin.register(Comment)
class CommentAdmin(ImportExportModelAdmin):
    resource_classes = [CommentResource]
    list_display = (
        'id',
        'review',
        'text',
        'author',
        'pub_date',
    )


@admin.register(GenreTitle)
class GenreTitleAdmin(ImportExportModelAdmin):
    resource_classes = [GenreTitleResource]
    list_display = (
        'id',
        'genre_id',
        'title_id',
    )
