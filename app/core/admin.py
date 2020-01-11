from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext as _
from core import models


class ProfileInline(admin.StackedInline):
    """To stack the user profile inline"""
    verbose_name_plural = 'Profile'
    model = models.UserProfile
    can_delete = False
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    ordering = ['id']
    list_display = [
        'email', 'username', 'is_superuser', 'is_staff', 'is_active'
    ]
    inlines = (ProfileInline, )
    search_fields = ['email', 'username']
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important Dates'), {'fields': ('last_login', )})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')
        }),
    )


class CustomUserProfile(admin.ModelAdmin):
    """Customizing the user profile admin page"""
    list_display = ['user', 'first_name', 'last_name',
                    'city', 'country', 'phone',
                    'primary_language', 'secondary_language',
                    'tertiary_language']
    search_fields = ['user', 'first_name',
                     'last_name', 'city', 'country',
                     'primary_language', 'secondary_language',
                     'tertiary_language']


admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.UserProfile, CustomUserProfile)
