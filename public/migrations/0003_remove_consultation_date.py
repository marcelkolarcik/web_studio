# Generated by Django 3.0.5 on 2020-09-17 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0002_auto_20200917_1757'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='consultation',
            name='date',
        ),
    ]
