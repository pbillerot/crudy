# Generated by Django 2.0.1 on 2018-02-02 18:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('whist', '0003_auto_20180202_1805'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='whistpartie',
            name='carte',
        ),
        migrations.RemoveField(
            model_name='whistpartie',
            name='jeu',
        ),
    ]
