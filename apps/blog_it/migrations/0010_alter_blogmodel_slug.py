# Generated by Django 3.2.10 on 2022-07-13 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog_it', '0009_alter_blogmodel_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogmodel',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
