from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.response import Response

from .serializers import UserSerializer, SignUpSerializer
from .permissions import IsAdmin
from reviews.models import User
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
