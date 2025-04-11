from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from users.models import User
from users.forms import UserCreationForm, UserChangeForm


class CustomUserAdmin(BaseUserAdmin):
    """Custom User Admin"""
    form = UserChangeForm
    add_form = UserCreationForm
    model = User

    list_display = ["email", "nickname", "is_staff", "is_superuser", "date_joined"]
    list_filter = ["is_staff", "is_superuser", "is_active"]
    readonly_fields = ["last_login", "date_joined"]

    fieldsets = (
        (None, {"fields": ("email", "nickname", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        ("Dates", {"fields": ("last_login", "date_joined")})
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide", ),
            "fields": ("email", "nickname", "password1", "password2"),
        }),
    )

    search_fields = ["email", "nickname"]
    ordering = ["-date_joined"]

admin.site.register(User, CustomUserAdmin)
