# Generated by Django 3.1.2 on 2020-12-08 14:39

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0040_auto_20201207_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='text',
            field=tinymce.models.HTMLField(),
        ),
    ]
