# Generated by Django 4.0.1 on 2022-05-24 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('attendanceapp', '0014_alter_testingmodel_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='testingmodel',
            old_name='photo',
            new_name='photo1',
        ),
    ]
