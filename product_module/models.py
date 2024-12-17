from django.db import models
from django.utils.timezone import now
from jalali_date import date2jalali, datetime2jalali
from django_jalali.db import models as jmodels
from jdatetime import datetime as jdatetime
from account_module.models import User
from django.core.exceptions import ValidationError

# Create your models here.


class Category(models.Model):

    title = models.CharField(max_length=120, verbose_name="عنوان")

    slug = models.SlugField(verbose_name='نشانی دسته بندی',
                            allow_unicode=True, unique=True)

    parent = models.ForeignKey(
        'category', on_delete=models.PROTECT, null=True, blank=True, related_name='sub_categoires')

    created_at = models.DateTimeField(
        verbose_name='زمان ساخت', auto_now_add=True)

    updated_at = models.DateTimeField(
        verbose_name='آخرین ویرایش', null=True, blank=True, auto_now=True)

    def jalali_created_at(self):
        return date2jalali(self.created_at)
    jalali_created_at.short_description = "تاریخ ایجاد"

    def jalali_updated_at(self):
        return datetime2jalali(self.updated_at)
    jalali_updated_at.short_description = "تاریخ آخرین ویرایش"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"


class Discount(models.Model):
    discount_percent = models.PositiveIntegerField(
        default=0, verbose_name='درصد تخفیف')

    discount_expire = jmodels.jDateTimeField(verbose_name="تاریخ انقضای تخفیف")

    discount_code = models.CharField(verbose_name='کد تخفیف' , max_length=10,null=True,blank=True,db_index=True,unique=True)


    def check_expire_discount(self):
        if  self.discount_expire > jdatetime.now().replace(microsecond=0):
            return True
        else:
            return False

    def get_discount_price(self, price):
        if self.check_expire_discount():
            temp = (price * self.discount_percent)/100
            return int(price - temp)

    def check_code(self,code,price):
        try:
            get_discount = Discount.objects.get(discount_code = code)
            if get_discount:
                if get_discount.check_expire_discount:
                    price = get_discount.get_discount_price(price)
                    return price
                else:
                    return False
            else:
                False
        except:
            return False


    get_discount_price.short_description = 'قیمت با تخفیف'

    def __str__(self):
        return f"{self.discount_percent}%"

    class Meta:
        verbose_name = 'تخفیف'
        verbose_name_plural = 'تخفیف ها'


class Product(models.Model):

    title = models.CharField(max_length=200, verbose_name='نام محصول')

    short_description = models.CharField(
        max_length=220, verbose_name='توضیح کوتاه', blank=True, null=True)

    description = models.TextField(verbose_name='توضیحات')

    price = models.IntegerField(
        verbose_name='قیمت', help_text="قیمت ها به تومان است")

    image = models.ImageField(verbose_name='عکس محصول',
                              upload_to="product/images")

    categories = models.ManyToManyField(Category, related_name='products')

    views = models.PositiveIntegerField(default=0, verbose_name='تعداد بازدید')

    discount = models.ForeignKey(Discount, on_delete=models.PROTECT, verbose_name='تخفیف', related_name="products", null=True,
                                 blank=True, help_text="درصورتی که برای محصول تخفیفی در نظر ندارید این بخش را نادیده بگیرید")

    pin_top = models.BooleanField(default=False, verbose_name='پین کردن محصول')

    slug = models.SlugField(verbose_name='نشانی محصول',
                            allow_unicode=True, unique=True)

    created_at = models.DateTimeField(
        verbose_name='زمان ساخت', auto_now_add=True)

    updated_at = models.DateTimeField(
        verbose_name='آخرین ویرایش', null=True, blank=True, auto_now=True)

    # functions




    def get_discount_price(self):

        if self.discount and self.discount.check_expire_discount():
            discount_price = self.discount.get_discount_price(self.price)
            if discount_price:
                return discount_price
            else:
                return self.price
        else:
            return False
    get_discount_price.short_description = 'قیمت با تخفیف'

    def fix_discount_state(self):
        if self.discount :
            if self.discount.check_expire_discount() == False:
                self.discount = None
                self.save()
                return self

    def format_price(self):
        return "{:,}".format(self.price)

    format_price.short_description = "قیمت"

    def format_discount_price(slef):
        return "{:,}".format(slef.get_discount_price())

    def jalali_created_at(self):
        return date2jalali(self.created_at)
    jalali_created_at.short_description = "تاریخ ایجاد"

    def jalali_updated_at(self):
        return datetime2jalali(self.updated_at)
    jalali_updated_at.short_description = "تاریخ آخرین ویرایش"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"


class ProductAttribute(models.Model):

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="attributes", verbose_name=" محصول")

    key = models.CharField(max_length=200, verbose_name="کلید")

    value = models.CharField(max_length=200, verbose_name="مقدار ")

    class Meta:
        verbose_name = "ویژگی محصول"
        verbose_name_plural = "ویژگی محصولات"
        unique_together = ['product', 'key']


class Blog(models.Model):

    title = models.CharField(max_length=120, verbose_name='عنوان')

    short_description = models.CharField(
        max_length=200, verbose_name='توضیح کوتاه')

    description = models.TextField(verbose_name='مقاله')

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, verbose_name='دسته بندی', related_name='blogs')

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blogs', verbose_name='نویسنده')

    image = models.ImageField(
        verbose_name='عکس مقاله', upload_to='blog/images')

    created_at = models.DateTimeField(
        verbose_name='زمان ساخت', auto_now_add=True)

    updated_at = models.DateTimeField(
        verbose_name='آخرین ویرایش', null=True, blank=True, auto_now=True)

    def jalali_created_at(self):
        return date2jalali(self.created_at).strftime("%y/%m/%d")
    jalali_created_at.short_description = "تاریخ ایجاد"

    def jalali_updated_at(self):
        return datetime2jalali(self.updated_at)
    jalali_updated_at.short_description = "تاریخ آخرین ویرایش"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقاله ها'


class Comment(models.Model):
    body = models.TextField(verbose_name='کامنت')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments', verbose_name='نویسنده')
    product = models.ForeignKey(
        Product, models.CASCADE, verbose_name='محصول', null=True, blank=True, related_name='comments')
    blog = models.ForeignKey(Blog, models.CASCADE, verbose_name='مقاله',
                             blank=True, null=True, related_name='comments')
    parent = models.OneToOneField(
        'Comment', models.CASCADE, verbose_name='کامنت پدر', null=True, blank=True, related_name='child')
    read_by_admin = models.BooleanField(default=False, verbose_name='خوانده شده توسط ادمین')
    visibel = models.BooleanField(default=False, verbose_name='نمایش داده شود / نشود')
    created_at = jmodels.jDateTimeField(verbose_name='تاریخ ایجاد')

    def __str__(self):
        return f"کاربر {self.author} نوشته : {self.body[:32]}"
    
    def save(self, *args , **keyworgs):
        self.created_at = jdatetime.now().replace(microsecond=0)
        return super().save(args,keyworgs)

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'
