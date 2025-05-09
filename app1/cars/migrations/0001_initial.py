# Generated by Django 5.2 on 2025-04-25 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cars',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='Название')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='URL')),
                ('description', models.TextField(verbose_name='Описание')),
                ('image', models.ImageField(upload_to='products_image', verbose_name='Изображение')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=7, verbose_name='Цена')),
            ],
            options={
                'verbose_name': 'Спец. технику',
                'verbose_name_plural': 'Спец. техники',
                'db_table': 'cars',
            },
        ),
    ]
