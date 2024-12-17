# Generated by Django 5.1.3 on 2024-12-11 20:47

import django.db.models.deletion
import django_jalali.db.models
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product_module', '0019_alter_comment_options_alter_comment_created_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=1, verbose_name='')),
                ('price', models.PositiveIntegerField(verbose_name='')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='product_module.product', verbose_name='')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_code', models.IntegerField(db_index=True, editable=False, unique=True, verbose_name='کدرهگیری')),
                ('total_price', models.PositiveIntegerField(verbose_name='قیمت کل')),
                ('state', models.BooleanField(default=False, verbose_name='وضعیت')),
                ('created_at', django_jalali.db.models.jDateTimeField(blank=True, null=True, verbose_name='تاریخ ایجاد')),
                ('check_out_date', django_jalali.db.models.jDateTimeField(blank=True, null=True, verbose_name='تاریخ تسویه')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
                ('items', models.ManyToManyField(to='cart_module.itemcart', verbose_name='محصولات')),
            ],
            options={
                'verbose_name': 'سبد خرید',
            },
        ),
    ]