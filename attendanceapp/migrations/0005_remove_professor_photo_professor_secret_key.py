# Generated by Django 4.0.1 on 2022-05-13 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0004_testingmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='professor',
            name='photo',
        ),
        migrations.AddField(
            model_name='professor',
            name='secret_key',
            field=models.CharField(default='', max_length=150),
        ),
    ]
