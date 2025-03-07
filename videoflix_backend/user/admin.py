from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from user.api.forms import CustomUserCreationForm
from user.models import CustomUser

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    fieldsets = (*UserAdmin.fieldsets,(
        'Individual Data',
        {
            'fields':(
                'phone',
                'address',
            )
        }
    ))

