from django.db import models
from product_module.models import Discount, Product
from account_module.models import User
from django_jalali.db import models as jmodels
from jdatetime import datetime as jdatetime
from random import randrange
# Create your models here.


class Cart(models.Model):
    tracking_code = models.IntegerField(
        verbose_name='کدرهگیری', editable=False, db_index=True, unique=True, primary_key=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='کاربر', related_name='carts')
    total_price = models.PositiveIntegerField(
        verbose_name='قیمت کل', default=0)
    state = models.BooleanField(default=False, verbose_name='وضعیت')
    discount = models.ForeignKey(
        Discount, on_delete=models.PROTECT, verbose_name='تخفیف', null=True, blank=True)
    created_at = jmodels.jDateTimeField(
        verbose_name='تاریخ ایجاد', null=True, blank=True)
    check_out_date = jmodels.jDateTimeField(
        verbose_name='تاریخ تسویه', null=True, blank=True)

    def calculating_total_price(self):
        items = self.items.all()
        if items:
            total = 0
            for item in items:
                total = total + item.price
            
            self.total_price = total
            self.save()
            
            return total

    def __str__(self):

        username = self.user.get_username()
        return f"{username}"

    def save(self, *args, **keywords):
        self.tracking_code = randrange(1000000, 9999999)
        self.created_at = jdatetime.now().replace(microsecond=0)
        return super().save(args, keywords)

    class Meta:
        verbose_name = "سبد خرید"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, verbose_name='سبد خرید', related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, verbose_name='سبد خرید', related_name='items', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        default=1, verbose_name='تعداد')
    price = models.IntegerField(verbose_name='قیمت')

    def total_price(self):
        price = 0
        if self.product.discount:
            price = self.product.get_discount_price()
        else:
            price = self.product.price

        return price * self.quantity

    def add_item_to_cart(cart: Cart, product: Product):
        price = 0
        if product.discount:
            price = product.get_discount_price()
        else:
            price = product.price

        item = CartItem.objects.create(
            cart=cart, product=product, price=price)
        
        cart.calculating_total_price()
        cart.save()

        return item

    def __str__(self):
        return self.product.title
