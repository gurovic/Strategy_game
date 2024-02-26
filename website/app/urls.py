from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import (sandbox_views, tournament_views, tournament_start_view, tournament_register_views,
                    game_upload_form_views, game_upload_compilation_views, game_upload_report_views)

urlpatterns = [
    path('sandbox/<int:game_id>', sandbox_views.show),
    path('tournament/', tournament_views.start_page, name="tounrament_startpage"),
    path('tournament/start/<int:tournament_id>', tournament_start_view.start_tournament),
    path('tournament/create/', tournament_views.create_tounament, name="create_tournament"),
    path('tournament/register/<int:tournament_id>/<int:user_id>', tournament_register_views.register),
    path('game_upload/form/', game_upload_form_views.GameUploadFormView.as_view(), name='game_upload_form'),
    path('game_upload/compilation/', game_upload_compilation_views.GameUploadCompilationView.as_view(), name='game_upload_compilation'),
    path('game_upload/report/', game_upload_report_views.GameUploadReportView.as_view(), name="game_upload_report")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
