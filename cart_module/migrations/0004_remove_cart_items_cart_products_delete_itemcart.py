# Generated by Django 5.1.3 on 2024-12-13 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_module', '0003_cart_discount_alter_cart_user'),
        ('product_module', '0020_discount_discount_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='items',
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(to='product_module.product', verbose_name='محصولات'),
        ),
        migrations.DeleteModel(
            name='ItemCart',
        ),
    ]
