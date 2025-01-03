# Generated by Django 5.1.3 on 2024-12-13 19:58

import django.db.models.deletion
import django_jalali.db.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cart_module', '0006_delete_cart'),
        ('product_module', '0020_discount_discount_code'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_code', models.IntegerField(db_index=True, editable=False, unique=True, verbose_name='کدرهگیری')),
                ('total_price', models.PositiveIntegerField(verbose_name='قیمت کل')),
                ('state', models.BooleanField(default=False, verbose_name='وضعیت')),
                ('created_at', django_jalali.db.models.jDateTimeField(blank=True, null=True, verbose_name='تاریخ ایجاد')),
                ('check_out_date', django_jalali.db.models.jDateTimeField(blank=True, null=True, verbose_name='تاریخ تسویه')),
                ('discount', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='product_module.discount', verbose_name='تخفیف')),
                ('products', models.ManyToManyField(blank=True, null=True, to='product_module.product', verbose_name='محصولات')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='carts', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'سبد خرید',
            },
        ),
    ]
