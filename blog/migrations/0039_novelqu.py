# Generated by Django 3.1 on 2021-05-01 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0038_chapterquepubs_novel'),
    ]

    operations = [
        migrations.CreateModel(
            name='NovelQu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('novel_title', models.CharField(default='default', max_length=500)),
                ('novel', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.novel')),
            ],
        ),
    ]