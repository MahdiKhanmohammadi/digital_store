# Generated by Django 5.1.3 on 2024-12-13 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_module', '0007_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='total_price',
            field=models.PositiveIntegerField(default=0, verbose_name='قیمت کل'),
        ),
    ]
