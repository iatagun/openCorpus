"""
Custom User Model for Government Corpus Platform
Implements role-based access control and audit logging
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class CustomUser(AbstractUser):
    """
    Extended user model with additional fields for government institution
    """
    
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Administrator')
        EDITOR = 'EDITOR', _('Editor')
        VIEWER = 'VIEWER', _('Viewer')
        RESEARCHER = 'RESEARCHER', _('Researcher')
    
    # Additional fields
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VIEWER,
        verbose_name=_('Role')
    )
    
    department = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Department')
    )
    
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Phone Number')
    )
    
    # Security fields
    is_approved = models.BooleanField(
        default=False,
        verbose_name=_('Approved'),
        help_text=_('Designates whether this user has been approved by an administrator.')
    )
    
    last_password_change = models.DateTimeField(
        default=timezone.now,
        verbose_name=_('Last Password Change')
    )
    
    # Two-Factor Authentication
    two_factor_enabled = models.BooleanField(
        default=False,
        verbose_name=_('2FA Enabled')
    )
    
    two_factor_secret = models.CharField(
        max_length=32,
        blank=True,
        verbose_name=_('2FA Secret')
    )
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-date_joined']
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def has_role(self, role):
        """Check if user has a specific role"""
        return self.role == role
    
    def can_edit_corpus(self):
        """Check if user can edit corpus data"""
        return self.role in [self.Role.ADMIN, self.Role.EDITOR]
    
    def can_approve_users(self):
        """Check if user can approve other users"""
        return self.role == self.Role.ADMIN


class UserProfile(models.Model):
    """
    Extended user profile with additional information
    """
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    
    bio = models.TextField(
        blank=True,
        verbose_name=_('Biography')
    )
    
    institution = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Institution')
    )
    
    title = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Title/Position')
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name=_('Avatar')
    )
    
    # Preferences
    email_notifications = models.BooleanField(
        default=True,
        verbose_name=_('Email Notifications')
    )
    
    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
    
    def __str__(self):
        return f"Profile of {self.user.username}"


class AuditLog(models.Model):
    """
    Audit log for tracking all user actions
    Essential for government compliance
    """
    
    class ActionType(models.TextChoices):
        LOGIN = 'LOGIN', _('Login')
        LOGOUT = 'LOGOUT', _('Logout')
        CREATE = 'CREATE', _('Create')
        UPDATE = 'UPDATE', _('Update')
        DELETE = 'DELETE', _('Delete')
        VIEW = 'VIEW', _('View')
        DOWNLOAD = 'DOWNLOAD', _('Download')
        UPLOAD = 'UPLOAD', _('Upload')
        APPROVE = 'APPROVE', _('Approve')
        REJECT = 'REJECT', _('Reject')
    
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='audit_logs'
    )
    
    action = models.CharField(
        max_length=20,
        choices=ActionType.choices,
        verbose_name=_('Action')
    )
    
    resource_type = models.CharField(
        max_length=100,
        verbose_name=_('Resource Type'),
        help_text=_('Type of resource affected (e.g., Document, User)')
    )
    
    resource_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Resource ID')
    )
    
    description = models.TextField(
        verbose_name=_('Description'),
        help_text=_('Detailed description of the action')
    )
    
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name=_('IP Address')
    )
    
    user_agent = models.TextField(
        blank=True,
        verbose_name=_('User Agent')
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Timestamp')
    )
    
    # Additional context
    extra_data = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('Extra Data')
    )
    
    class Meta:
        verbose_name = _('Audit Log')
        verbose_name_plural = _('Audit Logs')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
        ]
    
    def __str__(self):
        return f"{self.user} - {self.action} - {self.timestamp}"
