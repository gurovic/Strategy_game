from django.urls import path
from . import views

urlpatterns = [
    path('', views.sandbox_button, name='button'),
    path('sandbox/<int:id>', views.show),
]
