# Generated by Django 3.0.4 on 2020-06-26 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0018_auto_20200626_1545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='novel',
            name='uid',
            field=models.CharField(default='', editable=False, max_length=100),
        ),
    ]
