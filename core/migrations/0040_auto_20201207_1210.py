# Generated by Django 3.1.2 on 2020-12-07 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0039_auto_20201206_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='name',
            field=models.ImageField(upload_to='data'),
        ),
    ]