# Generated by Django 4.2.7 on 2023-11-27 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendors',
            name='on_time_delivery_rate',
            field=models.FloatField(null=True),
        ),
    ]
