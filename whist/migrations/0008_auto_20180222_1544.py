# Generated by Django 2.0.2 on 2018-02-22 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whist', '0007_auto_20180222_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='whistjeu',
            name='pari',
            field=models.IntegerField(default=0, verbose_name='Pari'),
        ),
    ]
