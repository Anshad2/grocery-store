# Generated by Django 5.0.1 on 2024-03-06 05:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gros', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_address', models.CharField(max_length=200)),
                ('phone', models.CharField(max_length=12)),
                ('email', models.CharField(max_length=255, null=True)),
                ('is_paid', models.BooleanField(default=False)),
                ('total', models.PositiveIntegerField()),
                ('user_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchase', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchaseitems', to='gros.order')),
            ],
        ),
    ]