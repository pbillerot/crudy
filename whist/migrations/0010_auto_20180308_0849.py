# Generated by Django 2.0.2 on 2018-03-08 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whist', '0009_auto_20180226_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='whistjeu',
            name='medal',
            field=models.IntegerField(default=0, verbose_name='Médaille'),
        ),
        migrations.AlterField(
            model_name='whistjeu',
            name='pari',
            field=models.IntegerField(default=0, verbose_name='Pari'),
        ),
        migrations.AlterField(
            model_name='whistpartie',
            name='cartes',
            field=models.IntegerField(default=0, help_text='Le nombre de cartes maximum par joueur qui seront distribuées', verbose_name='Nombre de cartes max / joueur'),
        ),
        migrations.AlterField(
            model_name='whistpartie',
            name='name',
            field=models.CharField(help_text='Le nom de la partie sera unique', max_length=50, verbose_name='Nom de la partie'),
        ),
    ]
