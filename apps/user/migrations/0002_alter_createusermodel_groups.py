# Generated by Django 3.2.10 on 2022-08-24 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='createusermodel',
            name='groups',
        ),
        migrations.AddField(
            model_name='createusermodel',
            name='groups',
            field=models.ManyToManyField(related_name='users', through='user.UserGroupRelation', to='user.UserGroupModel'),
        ),
    ]
