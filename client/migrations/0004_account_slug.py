# Generated by Django 4.2.7 on 2023-11-16 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_account_expenses_account_income'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='slug',
            field=models.SlugField(blank=True, max_length=120),
        ),
    ]
