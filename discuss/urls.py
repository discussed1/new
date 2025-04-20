"""
URL configuration for discuss project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('markdownx/', include('markdownx.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include('core.api.urls')),  # API endpoints
    path('silk/', include('silk.urls', namespace='silk')),  # Django Silk profiling
    # Override specific auth URLs with our consolidated templates
    path('accounts/', include('core.views.auth_urls')),
    # Include remaining allauth URLs
    path('accounts/', include('allauth.urls')),
    # path('avatar/', include('avatar.urls')),  # Replaced with native ImageField in Profile model
    # path('user-guide/', include('user_guide.urls')),  # User guide removed from application
    # Override postman URLs with our consolidated views
    path('messages/', include('core.views.messaging_urls', namespace='postman')),
    path('', include('core.urls')),
]

# Add Debug Toolbar URLs when in DEBUG mode
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# Serve media files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
