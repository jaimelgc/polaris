# Generated by Django 4.2.7 on 2023-11-12 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='product',
            name='created',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='body',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='slug',
            field=models.SlugField(blank=True, max_length=250),
        ),
        migrations.AddIndex(
            model_name='product',
            index=models.Index(fields=['-created'], name='guest_produ_created_a55fdf_idx'),
        ),
    ]
