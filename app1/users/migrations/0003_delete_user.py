# Generated by Django 5.2 on 2025-04-26 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_otchestvo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
