# Generated by Django 4.2.10 on 2024-02-19 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0017_alter_account_alias_alter_account_balance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='slug',
            field=models.SlugField(blank=True, max_length=120),
        ),
    ]
