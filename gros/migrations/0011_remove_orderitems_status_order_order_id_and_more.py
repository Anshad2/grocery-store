# Generated by Django 5.0.1 on 2024-03-31 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gros', '0010_remove_order_zipcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitems',
            name='status',
        ),
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.CharField(choices=[('cod', 'cod'), ('online', 'online')], default='cod', max_length=200),
        ),
        migrations.AddField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('order-placed', 'order-placed'), ('intransit', 'intransit'), ('dispatched', 'dispatched'), ('delivered', 'delivered'), ('cancelled', 'cancelled')], default='order-placed', max_length=200),
        ),
    ]
