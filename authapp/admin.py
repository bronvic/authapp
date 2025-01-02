from django.contrib import admin

from .models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "parent_username", "telegram_id", "is_active")
    search_fields = ("username", "email")
    list_filter = ("is_active",)
    readonly_fields = ("username", "parent_username", "telegram_id")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "parent_username",
                    "telegram_id",
                    "first_name",
                    "last_name",
                    "is_active",
                )
            },
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
