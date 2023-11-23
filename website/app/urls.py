from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import sandbox_views

urlpatterns = [
    path('sandbox/<int:id>', sandbox_views.show),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
