# Generated by Django 4.2.7 on 2023-11-16 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0005_alter_account_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='alias',
            field=models.CharField(max_length=120, unique=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='slug',
            field=models.SlugField(max_length=120),
        ),
    ]
