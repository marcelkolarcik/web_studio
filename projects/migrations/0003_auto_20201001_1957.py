# Generated by Django 3.1.1 on 2020-10-01 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20201001_1900'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='client_approved',
        ),
        migrations.RemoveField(
            model_name='project',
            name='development_link_sent',
        ),
        migrations.RemoveField(
            model_name='project',
            name='domain_hosting',
        ),
        migrations.RemoveField(
            model_name='project',
            name='done',
        ),
        migrations.RemoveField(
            model_name='project',
            name='started',
        ),
        migrations.RemoveField(
            model_name='project',
            name='started_on_site',
        ),
        migrations.RemoveField(
            model_name='project',
            name='update_after_wireframes',
        ),
        migrations.RemoveField(
            model_name='project',
            name='wireframes',
        ),
    ]