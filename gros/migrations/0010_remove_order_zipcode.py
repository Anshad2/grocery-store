# Generated by Django 5.0.1 on 2024-03-30 05:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gros', '0009_order_zipcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='zipcode',
        ),
    ]
