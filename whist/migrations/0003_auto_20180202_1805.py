# coding: utf-8
# Generated by Django 2.0.1 on 2018-02-02 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whist', '0002_whistjeu_carte'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whistjeu',
            name='jeu',
            field=models.IntegerField(default=0, verbose_name='N° du tour'),
        ),
    ]
