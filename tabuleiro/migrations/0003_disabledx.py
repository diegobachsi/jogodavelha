# Generated by Django 3.2.6 on 2022-08-29 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tabuleiro', '0002_auto_20220829_1336'),
    ]

    operations = [
        migrations.CreateModel(
            name='DisabledX',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('op1', models.CharField(default='1', max_length=1)),
                ('op2', models.CharField(default='2', max_length=1)),
                ('op3', models.CharField(default='3', max_length=1)),
                ('op4', models.CharField(default='4', max_length=1)),
                ('op5', models.CharField(default='5', max_length=1)),
                ('op6', models.CharField(default='6', max_length=1)),
                ('op7', models.CharField(default='7', max_length=1)),
                ('op8', models.CharField(default='8', max_length=1)),
                ('op9', models.CharField(default='9', max_length=1)),
            ],
        ),
    ]
