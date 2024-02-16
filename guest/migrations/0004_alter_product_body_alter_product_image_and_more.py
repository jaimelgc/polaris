# Generated by Django 4.2.10 on 2024-02-13 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0003_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='body',
            field=models.TextField(verbose_name='body'),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/%Y/%m/%d/', verbose_name='image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='subtitle',
            field=models.CharField(max_length=250, verbose_name='subtitle'),
        ),
        migrations.AlterField(
            model_name='product',
            name='title',
            field=models.CharField(max_length=250, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('ACC', 'Account'), ('CRD', 'Card')], max_length=3, verbose_name='type'),
        ),
    ]