# Generated by Django 3.1.2 on 2020-12-11 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_auto_20201209_1840'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='contours',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='image',
            name='edges',
            field=models.IntegerField(default=0),
        ),
    ]
