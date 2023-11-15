from django.contrib import admin
from django.urls import path
from ..app.views import compiler_report_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('compiler-report/<int:id>', boirs_views.show, name='compiler_report_details'),
    path('compiler-report', boirs_views.show_all, name='compiler_reports'),
]
