# Generated by Django 3.2 on 2022-05-08 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0002_auto_20220508_0740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentlineitem',
            name='car_price',
            field=models.IntegerField(),
        ),
    ]