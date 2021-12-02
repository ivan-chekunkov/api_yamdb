from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TitleViewSet, CategoryViewSet, GenreViewSet


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


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
