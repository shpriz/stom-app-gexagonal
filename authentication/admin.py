from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import UserProfile, UserSession


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    extra = 0
    fields = ('role', 'license_number', 'department', 'phone', 'is_active_staff')


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_active', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'profile__role', 'profile__is_active_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'profile__license_number')
    
    def get_role(self, obj):
        try:
            return obj.profile.get_role_display()
        except UserProfile.DoesNotExist:
            return "No Profile"
    get_role.short_description = 'Role'
    get_role.admin_order_field = 'profile__role'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'license_number', 'department', 'is_active_staff', 'created_at')
    list_filter = ('role', 'is_active_staff', 'department')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'license_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Role & Permissions', {
            'fields': ('role', 'license_number', 'department', 'is_active_staff')
        }),
        ('Contact Information', {
            'fields': ('phone',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'logout_time', 'ip_address', 'is_active')
    list_filter = ('is_active', 'login_time', 'user__profile__role')
    search_fields = ('user__username', 'ip_address', 'session_key')
    readonly_fields = ('session_key', 'login_time', 'logout_time', 'ip_address', 'user_agent')
    date_hierarchy = 'login_time'
    
    def has_add_permission(self, request):
        return False  # Sessions are created automatically
    
    def has_change_permission(self, request, obj=None):
        return False  # Sessions should not be modified manually


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
