# Generated by Django 2.0.2 on 2018-03-19 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whist', '0010_auto_20180308_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='whistjoueur',
            name='owner',
            field=models.CharField(default='inconnu', help_text='Le compte propriétaire', max_length=50, verbose_name='Compte'),
        ),
        migrations.AddField(
            model_name='whistpartie',
            name='owner',
            field=models.CharField(default='inconnu', help_text='Le compte propriétaire', max_length=50, verbose_name='Compte'),
        ),
    ]
