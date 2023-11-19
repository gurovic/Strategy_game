from django.urls import path
from .views import compiler_report_views
from .views import ideal_solution_test_views
from .views import game_views

urlpatterns = [
    path('compiler-report/<int:id>/', compiler_report_views.show, name='compiler_report_details'),
    path('compiler-report/', compiler_report_views.show_all, name='compiler_reports'),

    path('post-ideal-solution/new/<int:id>/', ideal_solution_test_views.post_new, name='ideal_solution_details'),

    path('post-game/new/', game_views.post_new, name='post_new_game'),
]
