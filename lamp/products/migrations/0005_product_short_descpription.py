# Generated by Django 4.0.2 on 2022-02-24 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='short_descpription',
            field=models.TextField(blank=True, default=None, null=True),
        ),
    ]
