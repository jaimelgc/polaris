# Generated by Django 4.2.10 on 2024-02-16 22:50

from django.db import migrations, models
import django.db.models.deletion
import parler.fields
import parler.models


class Migration(migrations.Migration):

    dependencies = [
        ('guest', '0004_alter_product_body_alter_product_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='body',
        ),
        migrations.RemoveField(
            model_name='product',
            name='subtitle',
        ),
        migrations.RemoveField(
            model_name='product',
            name='title',
        ),
        migrations.CreateModel(
            name='ProductTranslation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('subtitle', models.CharField(max_length=250, verbose_name='subtitle')),
                ('body', models.TextField(verbose_name='body')),
                ('master', parler.fields.TranslationsForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translations', to='guest.product')),
            ],
            options={
                'verbose_name': 'product Translation',
                'db_table': 'guest_product_translation',
                'db_tablespace': '',
                'managed': True,
                'default_permissions': (),
                'unique_together': {('language_code', 'master')},
            },
            bases=(parler.models.TranslatableModel, models.Model),
        ),
    ]