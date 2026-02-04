"""
Admin configuration for corpus app
"""

from django.contrib import admin
from .models import Category, Document, Compilation, AccessControl


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin"""
    
    list_display = ['name', 'parent', 'is_active', 'color']
    list_filter = ['is_active', 'parent']
    search_fields = ['name', 'description']
    list_editable = ['is_active']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Document admin with security features"""
    
    list_display = ['title', 'category', 'status', 'language', 'word_count', 
                   'is_sensitive', 'uploaded_by', 'created_at']
    list_filter = ['status', 'category', 'language', 'is_sensitive', 'is_encrypted', 'created_at']
    search_fields = ['title', 'description', 'content_text']
    readonly_fields = ['file_size', 'file_hash', 'word_count', 'char_count', 
                      'approved_by', 'approved_at', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category', 'language')
        }),
        ('File', {
            'fields': ('file', 'file_size', 'file_hash')
        }),
        ('Content', {
            'fields': ('word_count', 'char_count', 'content_text')
        }),
        ('Status', {
            'fields': ('status', 'approved_by', 'approved_at')
        }),
        ('Security', {
            'fields': ('is_encrypted', 'is_sensitive')
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Audit', {
            'fields': ('uploaded_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Compilation)
class CompilationAdmin(admin.ModelAdmin):
    """Compilation admin"""
    
    list_display = ['name', 'total_documents', 'total_words', 'is_public', 'created_by', 'created_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['name', 'description']
    filter_horizontal = ['documents']
    readonly_fields = ['total_documents', 'total_words', 'total_characters', 'created_at', 'updated_at']


@admin.register(AccessControl)
class AccessControlAdmin(admin.ModelAdmin):
    """Access control admin"""
    
    list_display = ['document', 'user', 'can_view', 'can_edit', 'can_delete', 'granted_by']
    list_filter = ['can_view', 'can_edit', 'can_delete']
    search_fields = ['document__title', 'user__username']
