# Generated by Django 3.1.2 on 2020-10-21 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_variant_is_right'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='slug',
            field=models.SlugField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='variant',
            name='is_right',
            field=models.BooleanField(verbose_name='Верный ответ?'),
        ),
    ]
