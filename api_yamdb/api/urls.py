from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, SignUpView


v1_router = DefaultRouter()
v1_router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/', include(v1_router.urls))
]
