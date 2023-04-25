from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet, SignUpView, CategoryViewSet, GenreViewSet, TitleViewSet
)


v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('categories', CategoryViewSet)
v1_router.register('genres', GenreViewSet)
v1_router.register('titles', TitleViewSet, basename='titles')


urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/', include(v1_router.urls))
]
