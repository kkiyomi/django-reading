# Generated by Django 3.1 on 2021-03-02 20:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0030_novel_original'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chapter',
            name='content',
        ),
        migrations.AddField(
            model_name='chapter',
            name='content_path',
            field=models.CharField(default='default', max_length=500),
        ),
        migrations.AlterField(
            model_name='chapter',
            name='title',
            field=models.CharField(max_length=500),
        ),
    ]
