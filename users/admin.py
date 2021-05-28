from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class CustomUserAdmin(UserAdmin):
    """Custom Admin User panel"""
    fieldsets = UserAdmin.fieldsets + (
        ("Custom User Details", {
            "fields": (
                "avatar",
                "is_seller"
            ),
        }),
    )
