from django.urls import include, path, re_path
from django.contrib import admin
from django.conf.urls.static import static
from . import settings
from . import healthz

urlpatterns = [
    re_path(r'^healthz/ready$', healthz.ready),
    re_path(r'^healthz/alive$', healthz.alive),
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # Main app URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
