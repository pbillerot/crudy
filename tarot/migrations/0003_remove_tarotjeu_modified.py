# Generated by Django 2.0.2 on 2018-03-30 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tarot', '0002_tarotpartie_modified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tarotjeu',
            name='modified',
        ),
    ]
