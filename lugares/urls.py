from django.urls import path
from . import views

urlpatterns = [
    path('recomendar/', views.recomendar_lugar, name='recomendar_lugar'),
    path('prueba/', views.prueba, name='prueba'),
    path('recomendar-2.0/', views.preguntas_view, name='preguntas'),
    path('resultado/', views.resultados_view, name='resultado'),
]