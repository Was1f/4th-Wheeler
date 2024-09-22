# create your views here
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Garage, Vehicle, Owner, User, Trip, Parking
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout


def rent_car(request):
 vehicles = Vehicle.objects.raw('SELECT licensenumber, modelname, color, seatcapacity, modelyear, type, ispremium FROM Vehicle')
 car_list = []
 for car in vehicles:
  fee_estimate = car.seatcapacity * 50
  car_list.append({
   'car': car,
   'fee_estimate': fee_estimate
  })
 return render(request, 'rentcar.html', {'car_list': car_list})


def rent_garage(request):
 garages = Garage.objects.raw('SELECT garageid, address, area, cctv, watchmen, slots FROM Garage')
 garage_list = []
 for garage in garages:
  fee_estimate = garage.slots * 400
  actual_fee = fee_estimate + 100
  garage_list.append({
   'garage': garage,
   'fee_estimate': fee_estimate,
   'actual_fee': actual_fee
  })
 return render(request, 'rentgarage.html', {'garage_list': garage_list})


from django.db import connection

def history(request):
 user_id = request.user.id
 with connection.cursor() as cursor:
  cursor.execute('''SELECT t.TripID, t.Start, t.End, v.ModelName, 
                   CASE WHEN v.IsPremium THEN 4000 ELSE 3000 END AS Cost
                   FROM Trip t
                   JOIN Vehicle v ON t.LicensePlate = v.LicenseNumber
                   WHERE t.CustomerID = %s''', [user_id])
  trips = cursor.fetchall()
 with connection.cursor() as cursor:
  cursor.execute('''SELECT p.ParkingID, p.Start, p.End, g.Address 
                   FROM Parking p
                   JOIN Garage g ON p.GarageID = g.GarageID
                   WHERE p.CustomerID = %s''', [user_id])
  parking_records = cursor.fetchall()
 return render(request, 'history.html', {'trips': trips, 'parking_records': parking_records})


@login_required
def user_profile(request):
 user_info = request.user
 return render(request, 'userprofile.html', {'user_info': user_info})

def logout_view(request):
 auth_logout(request)
 return redirect('login')
