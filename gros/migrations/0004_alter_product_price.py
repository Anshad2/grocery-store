# Generated by Django 5.0.1 on 2024-03-06 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gros', '0003_alter_product_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]