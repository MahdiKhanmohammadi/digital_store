from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    phone = models.CharField(
        verbose_name='تلفن', max_length=11, null=True, blank=True)
    address = models.TextField(verbose_name='آدرس', null=True, blank=True)
    verify_code = models.CharField(
        max_length=220, blank=True, editable=False, null=True, db_index=True)
