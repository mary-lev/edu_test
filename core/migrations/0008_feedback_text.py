# Generated by Django 3.1.2 on 2020-10-12 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20201012_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='text',
            field=models.TextField(null=True),
        ),
    ]
