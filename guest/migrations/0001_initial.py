# Generated by Django 4.2.7 on 2023-11-07 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('subtitle', models.CharField(max_length=250)),
                ('slug', models.SlugField(max_length=250)),
                ('body', models.TextField()),
                ('image', models.ImageField(blank=True, upload_to='products/%Y/%m/%d/')),
                ('type', models.CharField(choices=[('ACC', 'Account'), ('CRD', 'Card')], max_length=3)),
            ],
        ),
    ]
