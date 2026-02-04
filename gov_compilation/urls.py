"""
Main URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('corpus.urls')),  # Home page and corpus routes
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)

# Customize admin site
admin.site.site_header = "Corpus Platformu Yonetim Paneli"
admin.site.site_title = "Corpus Yonetim"
admin.site.index_title = "Sistem Yonetimi"

# Admin access restricted to ADMIN role only
# Users will be redirected via custom middleware if not authorized
