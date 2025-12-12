import time
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.text import slugify
from django.utils import timezone
from django.forms import ValidationError

from extenstions.utils import jalali_converter
from .managers import UserManager
from utils.validator import mobile_validator


def upload_image(instance, filename):
    path = f"uploads/users/{slugify(instance.phone_number, allow_unicode=True)}"
    name = f"{time.time()}-{instance.phone_number}-{filename}"
    return f"{path}/{name}"


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, verbose_name="نام")
    last_name = models.CharField(max_length=100, verbose_name="نام خانوادگی")

    phone_number = models.CharField(
        max_length=11,
        unique=True,
        validators=[mobile_validator],
        verbose_name="شماره تلفن"
    )

    email = models.EmailField(unique=True, null=True, blank=True, verbose_name="ایمیل")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")

    is_owner = models.BooleanField("مالک هست؟", default=False)
    is_active = models.BooleanField("فعال", default=True)
    is_staff = models.BooleanField("کارمند", default=False)

    # PermissionsMixin already has is_superuser
    image = models.ImageField(
        "تصویر", upload_to=upload_image, null=True, blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "کاربر"
        verbose_name_plural = "کاربران"

    def get_full_name(self):
        if self.first_name or self.last_name:
            return f"{self.first_name} {self.last_name}".strip()
        return self.phone_number

    get_full_name.short_description = "نام و نام خانوادگی"

    def jcreated(self):
        return jalali_converter(self.created_at)

    jcreated.short_description = "تاریخ ساخت"

    def jupdated(self):
        return jalali_converter(self.updated_at)

    jupdated.short_description = "تاریخ بروز رسانی"

    def get_avatar(self):
        return self.image.url if self.image else 'static/img/user-3.jpg'

    @property
    def has_birthday_today(self):
        if not hasattr(self, "birthday_day") or not hasattr(self, "birthday_month"):
            return False
        today = timezone.localdate()
        return today.day == self.birthday_day and today.month == self.birthday_month

    def __str__(self):
        return self.get_full_name()
