from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.models import User
from django.utils.translation import gettext_lazy as _
# Register your models here.

class VideoFlixUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_('Individual Data'),{'fields':('phone','address',)}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    readonly_fields = ("last_login", "date_joined")
    ordering = ("email",)

admin.site.register(User, VideoFlixUserAdmin)

