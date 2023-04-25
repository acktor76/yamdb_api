from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import (
    UserSerializer, SignUpSerializer, CategorySerializer, GenreSerializer,
    TitleViewSerializer, TitleSerializer
)
from .permissions import IsAdmin, IsStaffOrReadOnly
from .mixins import CDLViewSet
from reviews.models import User, Category, Genre, Title
from api_yamdb.settings import ADMIN_EMAIL


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)

    @action(methods=['GET', 'PATCH'], detail=False,
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        user = self.request.user
        if request.method == 'GET':
            serializer = UserSerializer(user)
        serializer = UserSerializer(user, request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        confirmation_code = default_token_generator.make_token(user)
        email_subject = 'Код для авторизации'
        email_text = f'Ваш код для авторизации - {confirmation_code}'
        admin_email = ADMIN_EMAIL
        user_email = user.email
        send_mail(email_subject, email_text, admin_email, user_email)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CDLViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class GenreViewSet(CDLViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'name', 'year')

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleViewSerializer
        return TitleSerializer
