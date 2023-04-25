from django.db import models
from rest_framework import serializers, validators
from reviews.models import User, Category, Genre, Title


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class CategorySerializer(serializers.ModelSerializer):
    slug = models.fields.SlugField(
        max_length=50,
        validators=[
            validators.UniqueValidator(
                queryset=Category.objects.all(),
                message='Slug не уникален.'),
        ]
    )

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    slug = models.fields.SlugField(
        max_length=50,
        validators=[
            validators.UniqueValidator(
                queryset=Genre.objects.all(),
                message='Slug не уникален.'),
        ]
    )

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleViewSerializer(serializers.ModelSerializer):
    # rating = 

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True,
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
