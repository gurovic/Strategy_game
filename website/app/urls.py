from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import sandbox_views, tournament_views
from .views.game_upload_views import GameUploadView

urlpatterns = [
    path('sandbox/<int:game_id>', sandbox_views.show),
    path('tournament/', tournament_views.start_page, name="tounrament_startpage"),
    path('tournament/create/', tournament_views.create_tounament, name="create_tournament"),
    path('game_upload/', GameUploadView.as_view(), name="game_upload")
    #path('sandbox', app.views.sandbox.run_SandboxForm, name='SandboxForm'),
    #path('sandbox/run/<int:id>', app.views.run_Sandbox),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
