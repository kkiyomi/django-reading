# Generated by Django 3.1 on 2021-05-01 16:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0039_novelqu'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapterquepubs',
            name='novel_qu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.novelqu'),
        ),
    ]
