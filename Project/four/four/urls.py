"""
URL configuration for four project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin

from django.urls import path
from rental import views

urlpatterns = [
    path('garages/', views.garage_list, name='garage_list'),
    path('vehicles/', views.vehicle_list, name='vehicle_list'),
    path('garage/add/', views.add_garage, name='add_garage'),
    path('vehicle/add/', views.add_vehicle, name='add_vehicle'),
    path('garage/edit/<int:garage_id>/', views.edit_garage, name='edit_garage'),
    path('vehicle/edit/<int:vehicle_id>/', views.edit_vehicle, name='edit_vehicle'),
]
