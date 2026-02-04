"""
Security utilities for encryption and file handling
"""

from cryptography.fernet import Fernet
from django.conf import settings
import hashlib
import os


class FileEncryption:
    """
    Handle file encryption and decryption using Fernet
    """
    
    def __init__(self):
        """Initialize with encryption key from settings"""
        key = settings.ENCRYPTION_KEY
        if isinstance(key, str):
            key = key.encode()
        self.cipher = Fernet(key)
    
    def encrypt_file(self, file_path):
        """
        Encrypt a file in place
        """
        with open(file_path, 'rb') as file:
            data = file.read()
        
        encrypted_data = self.cipher.encrypt(data)
        
        with open(file_path, 'wb') as file:
            file.write(encrypted_data)
        
        return True
    
    def decrypt_file(self, file_path):
        """
        Decrypt a file in place
        """
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()
        
        decrypted_data = self.cipher.decrypt(encrypted_data)
        
        with open(file_path, 'wb') as file:
            file.write(decrypted_data)
        
        return True
    
    def encrypt_data(self, data):
        """
        Encrypt raw data
        """
        if isinstance(data, str):
            data = data.encode()
        return self.cipher.encrypt(data)
    
    def decrypt_data(self, encrypted_data):
        """
        Decrypt raw data
        """
        if isinstance(encrypted_data, str):
            encrypted_data = encrypted_data.encode()
        return self.cipher.decrypt(encrypted_data)


def calculate_file_hash(file_path):
    """
    Calculate SHA256 hash of a file
    """
    sha256 = hashlib.sha256()
    
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    
    return sha256.hexdigest()


def get_file_size(file_path):
    """
    Get file size in bytes
    """
    return os.path.getsize(file_path)


def validate_file_extension(filename, allowed_extensions=None):
    """
    Validate file extension against allowed list
    """
    if allowed_extensions is None:
        allowed_extensions = settings.ALLOWED_UPLOAD_EXTENSIONS
    
    ext = os.path.splitext(filename)[1].lower()
    return ext in allowed_extensions


def sanitize_filename(filename):
    """
    Sanitize filename to prevent path traversal attacks
    """
    # Remove any directory path
    filename = os.path.basename(filename)
    
    # Remove potentially dangerous characters
    dangerous_chars = ['..', '/', '\\', ':', '*', '?', '"', '<', '>', '|']
    for char in dangerous_chars:
        filename = filename.replace(char, '_')
    
    return filename
