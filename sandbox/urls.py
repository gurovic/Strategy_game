from django.urls import path
from . import views

urlpatterns = [
    path('', views.run_SandboxForm, name='SandboxForm'),
    path('sandbox/<int:id>', views.run_Sandbox),
]
