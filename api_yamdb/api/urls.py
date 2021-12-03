from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views
from .views import UserViewSet

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', views.send_code_confirmation),
    path('v1/auth/token/', views.get_user_token_auth),
    path('v1/users/me', views.UserInfo),
]
