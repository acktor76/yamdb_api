# Generated by Django 3.2 on 2023-05-03 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_alter_title_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, default=' ', verbose_name='Описание'),
            preserve_default=False,
        ),
    ]
