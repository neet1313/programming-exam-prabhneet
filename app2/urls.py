from django.urls import path
from . import views

urlpatterns = [
    path('', views.bloch_sphere, name='bloch_sphere'),
]