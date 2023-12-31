from datetime import datetime

from rest_framework import serializers, validators

from reviews.models import (User, Category, Genre, Title, Review, Comment,
                            get_censored)
from reviews.validators import validate_username

MIN_SCORE = 1
MAX_SCORE = 10


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
        validate_username(value)
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
    slug = serializers.SlugField(
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
    slug = serializers.SlugField(
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
    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        return obj.get_rating()

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
    name = serializers.CharField(max_length=256)
    year = serializers.IntegerField(max_value=datetime.now().year, min_value=0)

    def validate_genre(self, data):
        if len(data) == 0:
            raise serializers.ValidationError("Не указан жанр")
        return data

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class TitleUpdateSerializer(TitleSerializer):
    def validate(self, data):
        if 'genre' in data:
            if len(data['genre']) == 0:
                raise serializers.ValidationError("Не указан жанр")
        return data


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
        if score < MIN_SCORE or score > MAX_SCORE:
            raise serializers.ValidationError(
                'Оценка должна быть от 1 до 10'
            )
        return score

    def validate_text(self, text):
        get_censored(text)
        return text


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        exclude = ('review',)
        read_only_fields = ('review', 'pub_date', 'id')
        model = Comment

    def validate_text(self, text):
        get_censored(text)
        return text
