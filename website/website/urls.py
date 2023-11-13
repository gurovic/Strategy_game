from django.contrib import admin
from django.urls import path
from ..app.views import boirs_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('get-compile-result/<int:id>', boirs_views.show),
]
