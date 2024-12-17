# Generated by Django 5.1.3 on 2024-12-16 15:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_module', '0008_alter_cart_total_price'),
        ('product_module', '0020_discount_discount_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1, verbose_name='تعداد')),
                ('price', models.IntegerField(verbose_name='قیمت')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='cart_module.cart', verbose_name='سبد خرید')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='product_module.product', verbose_name='سبد خرید')),
            ],
        ),
    ]