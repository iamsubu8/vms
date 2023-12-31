# Generated by Django 4.2.7 on 2023-11-27 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_vendors_on_time_delivery_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendors',
            name='average_response_time',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='vendors',
            name='fulfillment_rate',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='vendors',
            name='quality_rating_avg',
            field=models.FloatField(null=True),
        ),
    ]
