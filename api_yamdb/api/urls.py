from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.views import SignUpView, TokenView, UsersViewSet
from api.views import (GenreViewSet, CategoryViewSet, TitleViewSet,
                       CommentViewSet, ReviewViewSet)

router_v1 = DefaultRouter()

router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(r'titles/(?P<title_id>\d+)/reviews',
                   ReviewViewSet, basename='reviews')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comments')
router_v1.register('users', UsersViewSet, basename='users')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='sign_up'),
    path('v1/auth/token/', TokenView.as_view()),
]
