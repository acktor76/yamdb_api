from django.contrib import admin

from .models import Category, Genre, Title, User, Review


class GenreinTitle(admin.TabularInline):
    model = Title.genre.through


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    inlines = (GenreinTitle,)


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Review)
