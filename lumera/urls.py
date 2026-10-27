"""
Root URL configuration for Lumera Cosmetics.
Includes URLs for the store app, admin, and media files in debug mode.
"""

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin panel
    path('admin/', admin.site.urls),
    path('', include('lumera.store.urls')),
]

# Serve media files during development (uploaded product images)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)