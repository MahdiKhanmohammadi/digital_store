# Generated by Django 5.1.3 on 2024-12-12 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0019_alter_comment_options_alter_comment_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='discount_code',
            field=models.CharField(blank=True, db_index=True, max_length=10, null=True, unique=True, verbose_name='کد تخفیف'),
        ),
    ]