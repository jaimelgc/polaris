# Generated by Django 4.2.7 on 2023-11-11 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='kind',
            field=models.CharField(choices=[('INC', 'Incomming'), ('OUT', 'Outgoing'), ('PAY', 'Payment'), ('COM', 'Commission')], default='PAY', max_length=3),
            preserve_default=False,
        ),
    ]