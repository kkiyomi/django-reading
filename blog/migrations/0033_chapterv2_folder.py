# Generated by Django 3.1 on 2021-03-02 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0032_remove_chapterv2_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapterv2',
            name='folder',
            field=models.CharField(default='novel_chapters', max_length=500),
        ),
    ]
