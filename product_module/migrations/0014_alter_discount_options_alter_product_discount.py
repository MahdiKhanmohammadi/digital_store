# Generated by Django 5.1.3 on 2024-11-28 14:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0013_discount_remove_product_discount_expire_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='discount',
            options={'verbose_name': 'تخفیف', 'verbose_name_plural': 'تخفیف ها'},
        ),
        migrations.AlterField(
            model_name='product',
            name='discount',
            field=models.ForeignKey(blank=True, help_text='درصورتی که برای محصول تخفیفی در نظر ندارید این بخش را نادیده بگیرید', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='products', to='product_module.discount', verbose_name='تخفیف'),
        ),
    ]
