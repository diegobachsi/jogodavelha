# Generated by Django 3.2.6 on 2022-08-30 13:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tabuleiro', '0005_auto_20220830_1320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tabuleiro',
            old_name='jogada',
            new_name='campos',
        ),
        migrations.RemoveField(
            model_name='tabuleiro',
            name='simbolo',
        ),
    ]