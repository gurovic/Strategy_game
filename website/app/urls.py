from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import sandbox_views, tournament_views, tournament_start_view, tournament_register_views, tournament_results_view, tournament_registration_view

urlpatterns = [
    path('sandbox/<int:game_id>', sandbox_views.show),
    path('tournament/', tournament_views.start_page, name="tounrament_startpage"),
    path('tournament/start/<int:tournament_id>', tournament_start_view.start_tournament),
    path('tournament/create/', tournament_views.create_tounament, name="create_tournament"),
    path('tournament/register/<int:tournament_id>/<int:user_id>', tournament_register_views.register),
    path('tournament/<int:tournament_id>/results', tournament_results_view.show),
    path('tournament/<int:tournament_id>/registration', tournament_registration_view.register, name="registration_for_tournament")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
