# Generated by Django 4.2.7 on 2023-11-18 13:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0013_alter_account_alias'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='client.account'),
        ),
    ]
