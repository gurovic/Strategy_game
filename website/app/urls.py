from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


from .views import sandbox_views, tournament_views, tournament_register_views

urlpatterns = [
    path('sandbox/<int:game_id>', sandbox_views.show),
    path('tournament/', tournament_views.start_page, name="tounrament_startpage"),
    path('tournament/create/', tournament_views.create_tounament, name="create_tournament"),
    path('tournament/register/<int:tournament_id>/<int:user_id>', tournament_register_views.register)
    #path('sandbox', app.views.sandbox.run_SandboxForm, name='SandboxForm'),
    #path('sandbox/run/<int:id>', app.views.run_Sandbox),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
