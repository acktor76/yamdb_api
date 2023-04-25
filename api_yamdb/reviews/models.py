from django.db import models


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
