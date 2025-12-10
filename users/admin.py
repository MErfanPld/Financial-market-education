from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.utils.html import format_html
from django.utils.timezone import localtime
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "phone_number",
        "get_full_name",
        "is_owner",
        "is_staff",
        "is_active",
        "is_superuser",
        "jcreated",
    )
    list_display_links = ("phone_number",)

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "is_owner",
    )
    search_fields = ("phone_number", "first_name", "last_name")

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("مشخصات کاربر", {
            "fields": (
                "first_name", "last_name", "phone_number", "email", "password",
                "image"
            )
        }),
        ("سطح دسترسی", {
            "fields": ("is_active", "is_owner", "is_staff", "is_superuser")
        }),
        ("تاریخ‌ها", {
            "fields": ("created_at", "updated_at"),
        }),
    )

    def save_model(self, request, obj, form, change):
        try:
            if 'password' in form.changed_data:
                obj.password = make_password(obj.password)

            super().save_model(request, obj, form, change)

        except Exception as e:
            from django.contrib import messages
            messages.error(request, f"❌ خطا: {e}")
