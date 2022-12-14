# Generated by Django 3.2.6 on 2022-08-31 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabuleiro', '0008_jogos'),
    ]

    operations = [
        migrations.AddField(
            model_name='jogos',
            name='jogador_one',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jogos',
            name='jogador_two',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jogos',
            name='modalidade',
            field=models.CharField(default='', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jogos',
            name='vencedor',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
