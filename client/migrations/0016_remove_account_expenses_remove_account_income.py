# Generated by Django 4.2.7 on 2023-11-19 16:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0015_alter_card_account'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='expenses',
        ),
        migrations.RemoveField(
            model_name='account',
            name='income',
        ),
    ]
