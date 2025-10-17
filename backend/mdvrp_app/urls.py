from django.urls import path
from .views import calculate_routes

urlpatterns = [
    path('calculate/', calculate_routes, name='calculate_routes'),
]
