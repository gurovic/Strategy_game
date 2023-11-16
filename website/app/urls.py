from django.urls import path
from .views import compiler_report_views
from .views import ideal_solution_test_views

urlpatterns = [
    path('compiler-report/<int:id>/', compiler_report_views.show, name='compiler_report_details'),
    path('compiler-report/', compiler_report_views.show_all, name='compiler_reports'),

    path('post-ideal-solution/new/', ideal_solution_test_views.post_new, name='ideal_solution_details'),
]
