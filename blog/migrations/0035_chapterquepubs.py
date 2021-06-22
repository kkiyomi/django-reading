# Generated by Django 3.1 on 2021-04-13 22:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0034_auto_20210302_2231'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChapterQUepubs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('novel_title', models.CharField(default='default', max_length=500)),
                ('title', models.CharField(default='default', max_length=500)),
                ('number', models.CharField(max_length=100)),
                ('content_path', models.CharField(default='default', max_length=500)),
                ('folder', models.CharField(default='novel_quepubs', max_length=500)),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
