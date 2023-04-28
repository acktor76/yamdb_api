from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .validators import validate_username

MAX_CHAR = 30

ROLE_CHOICES = (('user', 'Пользователь'), ('moderator', 'Модератор'),
                ('admin', 'Администратор'))


class User(AbstractUser):
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        validators=(validate_username,)
    )
    email = models.EmailField(
        'Электронная почта',
        max_length=254,
        unique=True,
        blank=False,
        null=False
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )
    bio = models.TextField(
        'О себе',
        blank=True
    )
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default='user',
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_user(self):
        return self.role == 'user'


class Category(models.Model):
    name = models.CharField(
        'Наименование категории', max_length=256, unique=True
    )
    slug = models.SlugField(
        'Slug категории', max_length=50, unique=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.CharField(
        'Наименование жанра', max_length=256, unique=True
    )
    slug = models.SlugField(
        'Slug жанра', max_length=50, unique=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    name = models.CharField(
        'Название', max_length=256
    )
    year = models.PositiveSmallIntegerField(
        'Год выпуска',
    )
    description = models.TextField(
        'Описание', blank=True, null=True, default=''
    )
    category = models.ForeignKey(
        Category, related_name="titles", verbose_name='Категория',
        blank=True, null=True, on_delete=models.SET_NULL
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle', verbose_name='Жанры',
        blank=True
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name="title",
        verbose_name='Произведение'
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.CASCADE, related_name="genre",
        verbose_name='Жанр'
    )

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведений'
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'genre'],
                name='unique_constraint_title_genre'
            )
        ]


class Review(models.Model):
    author = models.ForeignKey(
        User, related_name='reviews', on_delete=models.CASCADE,
        verbose_name='Автор')
    title = models.ForeignKey(
        Title, related_name='reviews', on_delete=models.CASCADE,
        verbose_name='Произведение'
    )
    text = models.TextField('Текст отзыва')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True,
        db_index=True)
    score = models.IntegerField(
        'Оценка произведения',
        validators=[
            MinValueValidator(1, message='Оценка должна быть не меньше 1'),
            MaxValueValidator(10, message='Оценка должна быть не больше 10')
        ]
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [models.UniqueConstraint(
            fields=('author', 'title'), name='unique review'
        )
        ]

    def __str__(self):
        return self.text[:MAX_CHAR]


class Comment(models.Model):
    author = models.ForeignKey(
        User, related_name='comments', on_delete=models.CASCADE,
        verbose_name='Автор')
    review = models.ForeignKey(
        Review, related_name='comments', on_delete=models.CASCADE,
        verbose_name='Отзыв')
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:MAX_CHAR]
