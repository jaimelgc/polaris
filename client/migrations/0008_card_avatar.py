# Generated by Django 4.2.7 on 2023-11-16 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0007_alter_account_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='card/%Y/%m/%d/'),
        ),
    ]