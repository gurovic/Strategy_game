from django.urls import path
from .views import compiler_report_views
from .views import ideal_solution_test_views

urlpatterns = [
    path('compiler-report/<int:id>/', compiler_report_views.show, name='compiler_report_details'),
    path('compiler-report/', compiler_report_views.show_all, name='compiler_reports'),

    path('ideal-solutions/<int:id>', ideal_solution_test_views.show, name='ideal_solution_details'),
]
