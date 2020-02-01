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


class CustomDoctor(admin.ModelAdmin):
    """Customizing the doctor page in admin view"""
    list_display = ('user', )
    list_filters = ('speciality1', )
    fieldsets = (
        (None, {
            'fields': (
                'user',
            ),
        }),
        (_('Additional Details'), {
            'fields': (
                'experience', 'qualification', 'highlights'
            ),
        }),
        (_('Specialities'), {
            'fields': (
                'speciality1', 'speciality2', 'speciality3',
                'speciality4'
            ),
        }),
    )


class CustomProcedure(admin.ModelAdmin):
    """Customising the procedure page"""
    list_display = ('name', 'days_in_hospital',
                    'days_in_destination')
    search_fields = ('name', 'speciality',)
    list_filter = ('speciality', )
    fieldsets = (
        (None, {
            'fields': (
                'name', 'speciality'
            )
        }),
        (_('Duration'), {
            'fields': (
                'days_in_hospital', 'days_in_destination',
                'duration_minutes'
            )
        }),
        (_('Additional details'), {
            'fields': (
                'overview', 'other_details'
            )
        }),
    )


class HospitalLanguageInline(admin.StackedInline):
    """To stack the user profile inline"""
    verbose_name_plural = 'Hospital Languages'
    model = models.HospitalLanguage
    can_delete = False
    classes = ['collapse', ]


class HospitalAccreditation(admin.StackedInline):
    """To stack the user profile inline"""
    verbose_name_plural = 'Accreditations'
    model = models.Accreditation
    can_delete = False
    classes = ['collapse', ]


class HospitalProcedureInline(admin.StackedInline):
    """To stack the user profile inline"""
    verbose_name_plural = 'Hospital Procedures'
    model = models.HospitalProcedure
    can_delete = False
    classes = ['collapse', ]


class HospitalDoctorInline(admin.StackedInline):
    """To stack the user profile inline"""
    verbose_name_plural = 'Doctors'
    model = models.HospitalDoctor
    can_delete = False
    classes = ['collapse', ]


class HospitalServicesInline(admin.StackedInline):
    """To stack hospital services inline"""
    verbose_name_plural = 'Services'
    model = models.Service
    can_delete = False
    classes = ['collapse', ]


class CustomHospital(admin.ModelAdmin):
    """Customizing the hospital display page"""
    list_display = ('name', 'state', 'country', 'postal_code')
    search_fields = ('name', 'state', 'country', 'postal_code')
    list_filter = ('country', 'state')
    inlines = (HospitalAccreditation, HospitalDoctorInline,
               HospitalLanguageInline, HospitalProcedureInline,
               HospitalServicesInline)
    fieldsets = (
        (None, {
            'fields': (
                'name',
            ),
        }),
        (_('Address'), {
            'fields': (
                'state', 'country', 'postal_code',
                'street_name', 'location_details',
            ),
        }),
        (_('Additional details'), {
            'fields': (
                'overview', 'staff_details'
            ),
        }),
        (_('Images'), {
            'fields': (
                'image1', 'image2', 'image3', 'image4',
                'image5', 'image6', 'image7', 'image8',
                'image9', 'image10', 'image11', 'image12'
            ),
        }),
        (_('Approved by'), {
            'fields': (
                'content_approver_name',
            ),
        }),
    )


class CustomService(admin.ModelAdmin):
    """Customising the services admin view"""
    list_display = ('hospital', 'name')
    list_filter = ('hospital', )


class CustomAccreditation(admin.ModelAdmin):
    """Customising the services admin view"""
    list_display = ('hospital', 'name')
    list_filter = ('hospital', )


admin.site.register(models.User, CustomUserAdmin)
admin.site.register(models.UserProfile, CustomUserProfile)
admin.site.register(models.Doctor, CustomDoctor)
admin.site.register(models.Procedure, CustomProcedure)
admin.site.register(models.Speciality)
admin.site.register(models.Accreditation, CustomAccreditation)
admin.site.register(models.Service, CustomService)
admin.site.register(models.HospitalDoctor)
admin.site.register(models.Hospital, CustomHospital)
