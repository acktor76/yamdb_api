import os
import csv
import codecs

from django.apps import apps
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from reviews.models import User


def get_field_value(model, field, value):
    """Получение значение поля в зависимости от его типа."""

    field_object = model._meta.get_field(field)
    if field_object.related_model is User:
        return field_object.related_model.objects.get(pk=value)
    if field_object.is_relation:
        return int(value)
    return value


def import_csv(model, file):
    """Импорт файла."""

    path = os.path.join(settings.STATICFILES_DIRS[0], 'data')
    with codecs.open(f'{path}\\{file}', 'r', encoding='utf_8_sig') as data:
        csv_reader = csv.DictReader(data)
        item = model()
        for row in csv_reader:
            for field, value in row.items():
                item.__setattr__(field, get_field_value(item, field, value))
            item.save()


class Command(BaseCommand):
    help = """Импорт данных из CSV файлов.
           порядок загрузки:
           python manage.py import -a reviews -m Category -f category.csv
           python manage.py import -a reviews -m Genre -f genre.csv
           python manage.py import -a reviews -m Title -f titles.csv
           python manage.py import -a reviews -m GenreTitle -f genre_title.csv
           python manage.py import -a reviews -m User -f users.csv
           python manage.py import -a reviews -m Review -f review.csv
           python manage.py import -a reviews -m Comment -f comments.csv
           """

    def add_arguments(self, parser):
        parser.add_argument('-m', '--model', required=True,
                            help='имя модели, необходимо')
        parser.add_argument('-a', '--app',  required=True,
                            help='имя приложения, необходимо')
        parser.add_argument('-f', '--file', required=True,
                            help='имя файла для импорта, необходимо')

    def handle(self, *args, **options):
        try:
            import_csv(apps.get_model(options['app'], options['model']),
                       options['file'])
        except Exception as e:
            raise CommandError(e)

        self.stdout.write(
            self.style.SUCCESS(
                f'{options["file"]} успешно импортирован в {options["model"]}.'
            )
        )
