from rest_framework import viewsets, filters, mixins, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Genre, Category, Title, Review, Comment
from api.filters import TitleFilter
from api.serializers import (GenreSerializer, CategorySerializer,
                             ReviewSerializer,
                             TitleCreateSerializer, TitleListSerializer,
                             CommentSerializer,
                             TokenSerializer,
                             UserSerializer,
                             SignUpSerializer,
                             UserRestrictedSerializer)
from api.permissions import (IsAdminOrReadOnly, IsAdmin,
                             IsAuthorModeratorAdminOrReadOnly)
from users.models import User


class CreateDestroyListViewSet(mixins.CreateModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.ListModelMixin,
                               viewsets.GenericViewSet):
    pass


class GenreViewSet(CreateDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    search_fields = ['name']
    filter_backends = [filters.SearchFilter]


class CategoryViewSet(CreateDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    search_fields = ['name']
    filter_backends = [filters.SearchFilter]


class ReviewViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование рецензий."""

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorModeratorAdminOrReadOnly, ]

    def get_title(self):
        return get_object_or_404(Title, pk=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(viewsets.ModelViewSet):
    """Просмотр и редактирование комментариев."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorModeratorAdminOrReadOnly, ]

    def get_review(self):
        return get_object_or_404(Review, title_id=self.kwargs.get('title_id'),
                                 id=self.kwargs.get('review_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())


class TitleViewSet(viewsets.ModelViewSet):
    """Класс произведения, доступно только админу."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).all()
    serializer_class = TitleCreateSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    filterset_fields = ('genre__slug',)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleListSerializer
        return TitleCreateSerializer


class NewViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']


class SignUpView(APIView):
    queryset = User.objects.all()
    serializer = SignUpSerializer

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        email = serializer.data.get('email')
        user, _ = User.objects.get_or_create(
            username=username,
            email=email,
        )
        user.confirmation_code = default_token_generator.make_token(user)
        user.save()
        send_mail(
            'Your personal token',
            user.confirmation_code,
            'aaaaaaa@boba.com',
            [email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UsersViewSet(NewViewSet):
    queryset = User.objects.all().order_by('pk')
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = "username"
    filter_backends = [SearchFilter]
    search_fields = ('username',)

    @action(
        methods=('get', 'patch'),
        detail=False, url_path='me',
        url_name='self_account',
        permission_classes=[IsAuthenticated]
    )
    def self_account(self, request):
        """Просмотр и изменение своего аккаунта."""
        serializer = UserRestrictedSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.initial_data.get('username')
            user = get_object_or_404(User, username=username)
            confirmation_code = serializer.initial_data.get(
                'confirmation_code'
            )

            if user.confirmation_code != confirmation_code:
                return Response(
                    {"confirmation_code": "invalid"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            return Response({"token": f"{access_token}"})
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
