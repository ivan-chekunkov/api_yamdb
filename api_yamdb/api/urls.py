from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (TitleViewSet, CategoryViewSet, GenreViewSet, 
                    CommentViewSet, ReviewViewSet)


router_v1 = DefaultRouter()

router_v1.register(
    'title',
    TitleViewSet,
    basename='title',
)
router_v1.register(
    'category',
    CategoryViewSet,
    basename='category',
)
router_v1.register(
    'genre',
    GenreViewSet,
    basename='genre',
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
