# Generated by Django 4.1.3 on 2022-12-15 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_product_nmb'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity_in_stock',
            field=models.IntegerField(default=0),
        ),
    ]