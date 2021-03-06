# Generated by Django 3.1.1 on 2020-10-01 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_number', models.CharField(max_length=32)),
                ('started', models.BooleanField(default=False)),
                ('wireframes', models.BooleanField(default=False)),
                ('update_after_wireframes', models.BooleanField(default=False)),
                ('started_on_site', models.BooleanField(default=False)),
                ('development_link', models.BooleanField(default=False)),
                ('client_approved', models.BooleanField(default=False)),
                ('domain_hosting', models.BooleanField(default=False)),
                ('done', models.BooleanField(default=False)),
            ],
        ),
    ]
