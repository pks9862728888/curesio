from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'first_name', 'last_name', 'country']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Personal Information'),
            {'fields': ('first_name', 'last_name', 'phone',
                        'date_of_birth', 'city', 'country',
                        'postal_code', 'address')}
        ),
        (
            _('Languages'),
            {'fields': ('primary_language', 'secondary_language',
                        'tertiary_language')}
        ),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important Dates'), {'fields': ('last_login',)})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
