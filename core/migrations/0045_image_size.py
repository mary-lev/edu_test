# Generated by Django 3.1.2 on 2020-12-11 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_auto_20201211_1338'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='size',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
