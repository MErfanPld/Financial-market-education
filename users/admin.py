from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm


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
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("phone_number", "first_name", "last_name")

    readonly_fields = ("password",)

    fieldsets = (
        ("مشخصات کاربر", {
            "fields": (
                "phone_number",
                "first_name",
                "last_name",
                "email",
                "image",
            )
        }),
        ("دسترسی‌ها", {
            "fields": ("is_active", "is_staff", "is_superuser")
        }),
        ("رمز عبور", {
            "fields": ("password", "new_password")
        }),
        # ("تاریخ‌ها", {
        #     "fields": ("jcreated", "jupdated"),
        # }),
    )

    add_fieldsets = (
        ("ایجاد کاربر جدید", {
            "classes": ("wide",),
            "fields": (
                "phone_number",
                "first_name",
                "last_name",
                "email",
                "password1",
                "password2",
            ),
        }),
    )

    ordering = ("-id",)


