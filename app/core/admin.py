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


class DoctorProfileInline(admin.StackedInline):
    """To stock doctor profile if user is doctor"""
    verbose_name_plural = 'Additional details if user is doctor'
    model = models.Doctor
    can_delete = False
    fk_name = 'user'
    classes = ['collapse', ]


class CustomUserAdmin(UserAdmin):

    def activate_accounts(self, request, queryset):
        """Activates selected accounts"""
        queryset.update(is_active=True)

    def deactivate_accounts(self, request, queryset):
        """Deactivates selected accounts"""
        queryset.update(is_active=False)

    def add_staff_permission(self, request, queryset):
        """Adds staff permission to selected accounts"""
        queryset.update(is_staff=True)

    def remove_staff_permission(self, request, queryset):
        """Adds staff permission to selected accounts"""
        queryset.update(is_staff=False)

    activate_accounts.short_description = 'Activate accounts'
    deactivate_accounts.short_description = 'Deactivate accounts'
    add_staff_permission.short_descriptin = 'Add Staff permission'
    remove_staff_permission.short_descriptin = 'Remove Staff permission'

    ordering = ['id']
    list_display = [
        'email', 'username', 'is_superuser', 'is_staff', 'is_active',
        'is_doctor'
    ]
    list_filter = ('is_superuser', 'is_staff', 'is_doctor', 'is_active')
    inlines = (ProfileInline, DoctorProfileInline, )
    search_fields = ['email', 'username', ]
    actions = [
        activate_accounts,
        deactivate_accounts,
        add_staff_permission,
        remove_staff_permission
    ]
    fieldsets = (
        (
            None,
            {'fields': ('email', 'username', 'password')}
        ),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_doctor')}
        ),
        (
            _('Important Dates'),
            {'classes': ('collapse',), 'fields': ('last_login', )}
        )
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
    search_fields = ['user__username', 'first_name',
                     'last_name', 'city', 'country',
                     'primary_language', 'secondary_language',
                     'tertiary_language']
    list_filter = ('country', )
    fieldsets = (
        (
            _('Personal details'),
            {
                'fields': ('first_name', 'last_name', 'date_of_birth')
            }
        ),
        (
            _('Avatar'),
            {
                'fields': ('image', )
            }
        ),
        (
            _('Contact details'),
            {
                'fields': (
                    'phone', 'city', 'country', 'postal_code', 'address'
                )
            }
        ),
        (
            _('Language preferences'),
            {
                'fields': (
                    'primary_language',
                    'secondary_language',
                    'tertiary_language')
            }
        )
    )


admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.UserProfile, CustomUserProfile)
admin.site.register(models.Doctor)
