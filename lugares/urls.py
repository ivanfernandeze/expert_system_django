from django.urls import path
from . import views

urlpatterns = [
    path('recomendar/', views.recomendar_lugar, name='recomendar_lugar'),
]
