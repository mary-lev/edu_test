# Generated by Django 3.1.2 on 2020-10-14 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20201014_1141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedacks', to='core.student'),
        ),
    ]
