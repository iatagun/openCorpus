"""
Corpus Models for Government Compilation Platform
Handles corpus documents, categories, and compilation management
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import FileExtensionValidator
import os


class Category(models.Model):
    """
    Corpus category/classification
    """
    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name=_('Category Name')
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_('Description')
    )
    
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('Parent Category')
    )
    
    color = models.CharField(
        max_length=7,
        default='#3498db',
        verbose_name=_('Color'),
        help_text=_('Hex color code for UI')
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Active')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.name} > {self.name}"
        return self.name


class Document(models.Model):
    """
    Main corpus document model
    """
    
    class Status(models.TextChoices):
        DRAFT = 'DRAFT', _('Draft')
        PENDING = 'PENDING', _('Pending Review')
        APPROVED = 'APPROVED', _('Approved')
        REJECTED = 'REJECTED', _('Rejected')
    
    # Basic Info
    title = models.CharField(
        max_length=500,
        verbose_name=_('Title')
    )
    
    description = models.TextField(
        blank=True,
        verbose_name=_('Description')
    )
    
    # File
    file = models.FileField(
        upload_to='corpus_documents/%Y/%m/%d/',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['txt', 'pdf', 'doc', 'docx', 'rtf', 'odt', 'html', 'xml', 'json']
            )
        ],
        verbose_name=_('Document File')
    )
    
    file_size = models.BigIntegerField(
        default=0,
        verbose_name=_('File Size (bytes)')
    )
    
    file_hash = models.CharField(
        max_length=64,
        blank=True,
        verbose_name=_('File Hash (SHA256)'),
        help_text=_('For integrity verification')
    )
    
    # Metadata
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='documents',
        verbose_name=_('Category')
    )
    
    language = models.CharField(
        max_length=10,
        default='tr',
        verbose_name=_('Language'),
        help_text=_('ISO 639-1 code')
    )
    
    word_count = models.IntegerField(
        default=0,
        verbose_name=_('Word Count')
    )
    
    char_count = models.IntegerField(
        default=0,
        verbose_name=_('Character Count')
    )
    
    # Status & Workflow
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name=_('Status')
    )
    
    # User tracking
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='uploaded_documents',
        verbose_name=_('Uploaded By')
    )
    
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_documents',
        verbose_name=_('Approved By')
    )
    
    approved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_('Approved At')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Security
    is_encrypted = models.BooleanField(
        default=False,
        verbose_name=_('Encrypted')
    )
    
    is_sensitive = models.BooleanField(
        default=False,
        verbose_name=_('Sensitive Data'),
        help_text=_('Marks document as containing sensitive information')
    )
    
    # Full-text search
    content_text = models.TextField(
        blank=True,
        verbose_name=_('Extracted Text'),
        help_text=_('Extracted text for search indexing')
    )
    
    # Metadata JSON
    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_('Additional Metadata')
    )
    
    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['category', '-created_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_file_extension(self):
        """Get file extension"""
        return os.path.splitext(self.file.name)[1].lower()


class Compilation(models.Model):
    """
    Collection of documents forming a corpus compilation
    """
    name = models.CharField(
        max_length=300,
        unique=True,
        verbose_name=_('Compilation Name')
    )
    
    description = models.TextField(
        verbose_name=_('Description')
    )
    
    documents = models.ManyToManyField(
        Document,
        related_name='compilations',
        verbose_name=_('Documents')
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_compilations',
        verbose_name=_('Created By')
    )
    
    is_public = models.BooleanField(
        default=False,
        verbose_name=_('Public'),
        help_text=_('Make this compilation publicly accessible')
    )
    
    # Statistics (cached for performance)
    total_documents = models.IntegerField(
        default=0,
        verbose_name=_('Total Documents')
    )
    
    total_words = models.BigIntegerField(
        default=0,
        verbose_name=_('Total Words')
    )
    
    total_characters = models.BigIntegerField(
        default=0,
        verbose_name=_('Total Characters')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('Compilation')
        verbose_name_plural = _('Compilations')
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    def update_statistics(self):
        """Update cached statistics"""
        docs = self.documents.all()
        self.total_documents = docs.count()
        self.total_words = sum(d.word_count for d in docs)
        self.total_characters = sum(d.char_count for d in docs)
        self.save()


class AccessControl(models.Model):
    """
    Document-level access control
    """
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='access_controls'
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='document_accesses'
    )
    
    can_view = models.BooleanField(default=True)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    
    granted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='granted_accesses'
    )
    
    granted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('Access Control')
        verbose_name_plural = _('Access Controls')
        unique_together = ['document', 'user']
    
    def __str__(self):
        return f"{self.user} - {self.document}"
