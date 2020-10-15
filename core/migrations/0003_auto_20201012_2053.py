# Generated by Django 3.1.2 on 2020-10-12 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20201012_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='lesson',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='core.lesson'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='core.task'),
        ),
    ]