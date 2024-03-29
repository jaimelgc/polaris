# Generated by Django 4.2.10 on 2024-02-13 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0016_remove_account_expenses_remove_account_income'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='alias',
            field=models.CharField(max_length=120, verbose_name='alias'),
        ),
        migrations.AlterField(
            model_name='account',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='balance'),
        ),
        migrations.AlterField(
            model_name='account',
            name='status',
            field=models.CharField(choices=[('AC', 'Active'), ('BL', 'Bloqued'), ('TE', 'Terminated')], default='AC', max_length=2, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='card',
            name='alias',
            field=models.CharField(max_length=120, verbose_name='alias'),
        ),
        migrations.AlterField(
            model_name='card',
            name='image',
            field=models.ImageField(blank=True, default='card.png', upload_to='card/%Y/%m/%d/', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='card',
            name='status',
            field=models.CharField(choices=[('AC', 'Active'), ('BL', 'Bloqued'), ('TE', 'Terminated')], default='AC', max_length=2, verbose_name='status'),
        ),
        migrations.AlterField(
            model_name='client',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='users/%Y/%m/%d/', verbose_name='avatar'),
        ),
        migrations.AlterField(
            model_name='client',
            name='status',
            field=models.CharField(choices=[('AC', 'Active'), ('BL', 'Bloqued'), ('TE', 'Terminated')], default='AC', max_length=2, verbose_name='status'),
        ),
    ]
