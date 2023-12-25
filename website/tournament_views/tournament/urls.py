from django.urls import path
from . import views

urlpatterns = [
    path('', views.start_page, name="tounrament_startpage"),
    path('create/', views.create_tounament, name="create_tournament")
]