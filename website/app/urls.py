from django.urls import path
from .views import compiler_report_views

urlpatterns = [
    path('compiler-report/<int:id>/', compiler_report_views.show, name='compiler_report_details'),
    path('compiler-report/', compiler_report_views.show_all, name='compiler_reports'),
]
