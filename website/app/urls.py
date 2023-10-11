from django.urls import path
from .views import battle_views

urlpatterns = [
    path('files/', battle_views.file_upload, name='file_upload'),
    path('files/success/', battle_views.file_upload, name='file_upload_success'),
    path('uploads/', battle_views.list_uploads, name='list_uploads'),
]
