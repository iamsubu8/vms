# Generated by Django 4.2.7 on 2023-11-27 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_vendors_average_response_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='po',
            name='po_number',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]