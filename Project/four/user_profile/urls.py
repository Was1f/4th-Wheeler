from django.urls import path
from . import views

urlpatterns = [
    path('user_profile/', views.user_profile, name='user_profile'),
    path('rent_car/', views.rent_car, name='car'),
    path('rent_garage/', views.rent_garage, name='garage'),
    path('login/', views.login, name='login'),
    path('history/', views.history, name='history'),


]

