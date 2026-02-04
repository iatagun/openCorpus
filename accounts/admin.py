"""
Admin configuration for accounts app
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, UserProfile, AuditLog


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Custom user admin with role management"""
    
    list_display = ['username', 'email', 'role', 'is_approved', 'is_active', 'date_joined']
    list_filter = ['role', 'is_approved', 'is_active', 'two_factor_enabled']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'department']
    
    fieldsets = UserAdmin.fieldsets + (
        (_('Role & Permissions'), {
            'fields': ('role', 'is_approved', 'department')
        }),
        (_('Security'), {
            'fields': ('two_factor_enabled', 'last_password_change')
        }),
        (_('Contact'), {
            'fields': ('phone_number',)
        }),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        (_('Additional Info'), {
            'fields': ('role', 'email', 'department')
        }),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """User profile admin"""
    
    list_display = ['user', 'institution', 'title']
    search_fields = ['user__username', 'institution', 'title']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    """Audit log admin - read-only for security"""
    
    list_display = ['timestamp', 'user', 'action', 'resource_type', 'ip_address']
    list_filter = ['action', 'resource_type', 'timestamp']
    search_fields = ['user__username', 'description', 'ip_address']
    readonly_fields = ['user', 'action', 'resource_type', 'resource_id', 
                      'description', 'ip_address', 'user_agent', 'timestamp', 'extra_data']
    
    def has_add_permission(self, request):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
