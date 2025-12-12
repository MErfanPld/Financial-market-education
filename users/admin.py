from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = (
        "phone_number",
        "get_full_name",
        "is_active",
        "is_staff",
        "is_superuser",
        "jcreated",
    )

    list_display_links = ("phone_number",)

    fieldsets = (
        ("مشخصات", {
            "fields": ("phone_number", "first_name", "last_name", "email", "image")
        }),
        ("دسترسی‌ها", {
            "fields": ("is_active", "is_staff", "is_superuser")
        }),
        ("رمز عبور", {
            "fields": ("new_password",)
        }),
    )

    add_fieldsets = (
        ("ایجاد کاربر جدید", {
            "classes": ("wide",),
            "fields": ("phone_number", "first_name", "last_name", "email", "password1", "password2"),
        }),
    )

    search_fields = ("phone_number", "first_name", "last_name")
    ordering = ("-id",)
