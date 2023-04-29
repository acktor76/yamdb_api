from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import LimitOffsetPagination

from .serializers import (
    UserSerializer, SignUpSerializer, TokenSerializer, CategorySerializer,
    GenreSerializer, TitleViewSerializer, TitleSerializer, ReviewSerializer,
    CommentSerializer
)
from .permissions import IsAdmin, IsStaffOrReadOnly
from .mixins import CDLViewSet
from .filters import TitleFilter
from reviews.models import User, Category, Genre, Title, Review, Comment
from api_yamdb.settings import ADMIN_EMAIL


class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('id')
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


class GetTokenView(APIView):
    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        user = get_object_or_404(User, username=username)
        confirmation_code = serializer.data['confirmation_code']
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        token = RefreshToken.for_user(user)
        return Response(
            {'token': str(token.access_token)},
            status=status.HTTP_200_OK
        )


class CategoryViewSet(CDLViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class GenreViewSet(CDLViewSet):
    queryset = Genre.objects.all().order_by('id')
    serializer_class = GenreSerializer
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    queryset = Title.objects.all().order_by(
        'id').annotate(rating=Avg('reviews__score'))
    permission_classes = (IsStaffOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return TitleViewSerializer
        return TitleSerializer


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsStaffOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_title(self, title_id):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return Review.objects.filter(title=self.get_title())

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsStaffOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_title(self, title_id):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_review(self, review_id):
        return get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                 title=self.get_title())

    def get_queryset(self):
        return Comment.objects.filter(review=self.get_review())

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user, review=self.get_review())
