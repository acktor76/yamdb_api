from django.db import models
import re

from rest_framework import serializers, validators

from reviews.models import User, Category, Genre, Title, Review, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role'
        )


class SignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=150,
    )
    email = serializers.EmailField(
        max_length=254
    )

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать "me" в качестве имени'
                'пользователя')
        if re.search(r'^[a-zA-Z][a-zA-Z0-9-_\.]{1,20}$', value) is None:
            raise serializers.ValidationError(
                f'В username недопустимый символ {value}'
            )
        return value

    class Meta:
        model = User
        fields = ('username', 'email')


class TokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


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
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'genre', 'category', 'rating'
        )


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True,
    )
    name = models.fields.CharField(max_length=256)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )

    class Meta:
        exclude = ('title',)
        read_only_fields = ('pub_date', 'id')
        model = Review

    def validate(self, attrs):
        author = self.context.get('request').user
        title = self.context.get('view').kwargs.get('title_id')
        if (Review.objects.filter(author=author, title=title).exists()
                and self.context.get('request').method == 'POST'):
            raise serializers.ValidationError(
                'Можно оставить только один отзыв на произведение'
            )
        return attrs

    def validate_score(self, score):
        if score < 1 or score > 10:
            raise serializers.ValidationError(
                'Оценка должна быть от 1 до 10'
            )
        return score


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        exclude = ('review',)
        read_only_fields = ('review', 'pub_date', 'id')
        model = Comment
