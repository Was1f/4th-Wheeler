
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from rental import views
from Reglogin import views as regview
from user_profile import views as user_views
from confirm import views as cv



urlpatterns = [
    #login
    path('admin', admin.site.urls),
    path('signup', regview.signup,name="signup"),
    path('login', regview.login,name="login"),
    #mimo

    path('user_profile/', user_views.user_profile, name='user_profile'),
    path('rent_car/', user_views.rent_car, name='car'),
    path('rent_garage/', user_views.rent_garage, name='garage'),
    path('logout/', user_views.logout_view, name='logout'),
    path('become_owner/', user_views.logout_view, name='become_owner'),
    path('history/', user_views.history, name='history'),

    #wasif
    path('ownerdb/', views.owner_dashboard, name='owner_dashboard'),
    path('owner_add/', views.owner_add, name='owner_add'),
    path('garage/edit/<int:garage_id>/', views.edit_garage, name='edit_garage'),
    path('vehicle/edit/<int:vehicle_id>/', views.edit_vehicle, name='edit_vehicle'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    #Ruby
    path('reservation', cv.reservation_view, name='reservation_form'),
    path('destination', cv.destination_view, name='destination_form'),
]