# Generated by Django 3.1 on 2021-02-14 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0028_auto_20200827_0434'),
    ]

    operations = [
        migrations.AddField(
            model_name='novel',
            name='wid',
            field=models.CharField(default='None', max_length=100),
        ),
    ]
