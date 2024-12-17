from django.db import models
from django_jalali.db import models as jmodels
from jdatetime import datetime as jdatetime
from django.core.exceptions import BadRequest,ValidationError
# Create your models here.

class Ad(models.Model):
    url = models.URLField(verbose_name='آدرس')
    title = models.CharField(max_length=120,verbose_name='عنوان',null=True,blank=True)
    image = models.ImageField(upload_to="ad/banner",verbose_name='بنر')
    visibel = models.BooleanField(default=False,verbose_name='نمایش داده شود /نشود')
    expire_date = jmodels.jDateTimeField(verbose_name='تاریخ انقضا')

    def check_expire_date(self):
        if self.visibel == True and self.expire_date<jdatetime.now().replace(microsecond=0):
            return True
        else:
            return False

    def __str__(self):
        return self.url
    
    def clean(self):
         if self.check_expire_date() == False:
             raise ValidationError({'expire_date':"تاریخ انقضا نمیتواند از تاریخ جاری قبل تر باشد"})
    

    # def save(self, *args,**keywords):
    #     if self.check_expire_date() == False:
    #         raise ValidationError("تاریخ انقضا نمیتواند از تاریخ جاری قبل تر باشد")
    #     else:
    #         return super().save(args,keywords)
    

    class Meta:
        verbose_name = 'تبلیغ'
        verbose_name_plural = 'تبلیغات'