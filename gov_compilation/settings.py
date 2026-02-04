"""
Django settings for gov_compilation project.
Secure configuration for government corpus compilation platform.
"""

from pathlib import Path
import environ
import os

# Initialize environment variables
env = environ.Env(
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Read .env file if it exists
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# SECURITY SETTINGS
# ==============================================================================

# SECRET_KEY - Generate a new one for production!
SECRET_KEY = env('SECRET_KEY', default='django-insecure-CHANGE-ME-IN-PRODUCTION')

# DEBUG - Should be False in production
DEBUG = env.bool('DEBUG', default=True)

# ALLOWED_HOSTS
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Session Security
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_SAVE_EVERY_REQUEST = True

# CSRF Protection
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SAMESITE = 'Strict'

# In production with HTTPS, enable these:
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Application definition
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    # 'django_ratelimit',  # Disabled for dev - requires Redis/Memcached
    'axes',
    
    # Local apps
    'accounts',
    'corpus',
    'security',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Custom security middleware
    'axes.middleware.AxesMiddleware',  # Brute force protection
    'security.admin_access.AdminAccessMiddleware',  # Admin access control
]

ROOT_URLCONF = 'gov_compilation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'gov_compilation.wsgi.application'

# Database
# ==============================================================================
# Using SQLite for local development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# For production with MySQL, uncomment below and update .env:
# DATABASES = {
#     'default': {
#         'ENGINE': env('DB_ENGINE', default='django.db.backends.mysql'),
#         'NAME': env('DB_NAME', default='corpus_db'),
#         'USER': env('DB_USER', default='root'),
#         'PASSWORD': env('DB_PASSWORD', default=''),
#         'HOST': env('DB_HOST', default='localhost'),
#         'PORT': env('DB_PORT', default='3306'),
#         'OPTIONS': {
#             'charset': 'utf8mb4',
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         },
#     }
# }

# Password validation
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 12,  # Strong password requirement
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Use Argon2 for password hashing (more secure than default)
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]

# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesStandaloneBackend',  # Axes first
    'django.contrib.auth.backends.ModelBackend',
]

# Custom User Model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Django Axes (Brute Force Protection)
# ==============================================================================
AXES_FAILURE_LIMIT = 5  # Lock after 5 failed attempts
AXES_COOLOFF_TIME = 1  # 1 hour lockout
AXES_LOCK_OUT_AT_FAILURE = True
AXES_ENABLE_ADMIN = True

# Django REST Framework
# ==============================================================================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}

# Cache Configuration
# ==============================================================================
# For development, using dummy cache. For production, use Redis or Memcached
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# Internationalization
# ==============================================================================

LANGUAGE_CODE = 'tr-tr'  # Turkish for government institution

TIME_ZONE = 'Europe/Istanbul'  # Turkey timezone

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# ==============================================================================

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files (User uploads)
# ==============================================================================

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 52428800  # 50MB

# Allowed file types for corpus documents
ALLOWED_UPLOAD_EXTENSIONS = [
    '.txt', '.pdf', '.doc', '.docx', '.rtf',
    '.odt', '.html', '.xml', '.json'
]

# Default primary key field type
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging Configuration
# ==============================================================================

LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'django.log',
            'formatter': 'verbose',
        },
        'security_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': LOGS_DIR / 'security.log',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'security': {
            'handlers': ['security_file'],
            'level': 'INFO',
            'propagate': False,
        },
        'axes': {
            'handlers': ['security_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Encryption Configuration
# ==============================================================================

ENCRYPTION_KEY = env('ENCRYPTION_KEY', default='')

# If no encryption key exists, we'll generate one on first run
if not ENCRYPTION_KEY:
    from cryptography.fernet import Fernet
    ENCRYPTION_KEY = Fernet.generate_key().decode()
    # In production, save this to environment variables!
    if DEBUG:
        key_file = BASE_DIR / 'encryption_key.txt'
        if not key_file.exists():
            key_file.write_text(ENCRYPTION_KEY)
