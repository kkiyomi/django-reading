# Generated by Django 3.0.4 on 2020-03-21 20:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_genre_slug'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]
