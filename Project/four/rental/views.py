from django.shortcuts import render, get_object_or_404, redirect
from django.db import connection
from .models import Garage, Vehicle
from .forms import GarageForm, VehicleForm
from django.contrib.auth.decorators import login_required

def execute_sql(sql, params=None):
    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        return cursor.fetchall()

@login_required
def vehicle_list(request):
    if hasattr(request.user, 'owner'):
        sql = "SELECT * FROM Vehicle WHERE OwnerID = %s"
        vehicles = execute_sql(sql, [request.user.owner.OwnerID])
        return render(request, 'vehicle_list.html', {'vehicles': vehicles})
    else:
        return render(request, 'error.html', {'message': 'You are not an owner.'})

def owner_dashboard(request):
    sql_garages = "SELECT * FROM Garage"
    garages = execute_sql(sql_garages)

    sql_vehicles = "SELECT * FROM Vehicle"
    vehicles = execute_sql(sql_vehicles)

    return render(request, 'o_db.html', {'garages': garages, 'vehicles': vehicles})

def owner_add(request):
    if request.method == 'POST':
        garage_form = GarageForm(request.POST)
        vehicle_form = VehicleForm(request.POST)

        if 'add_garage' in request.POST and garage_form.is_valid():
            garage = garage_form.save(commit=False)
            sql = "INSERT INTO Garage (Slots, CCTV, Watchmen, Area, Address, OwnerID) VALUES (%s, %s, %s, %s, %s, %s)"
            
            params = (garage.Slots, garage.CCTV, garage.Watchmen, garage.Area, garage.Address, request.user.owner.OwnerID)
            print(params)
            execute_sql(sql, params)
            return redirect('garage_and_vehicle_list')

        if 'add_vehicle' in request.POST and vehicle_form.is_valid():
            vehicle = vehicle_form.save(commit=False)
            sql = "INSERT INTO Vehicle (LicenseNumber, ModelName, Color, SeatCapacity, ModelYear, Type, IsPremium, OwnerID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            params = (vehicle.LicenseNumber, vehicle.ModelName, vehicle.Color, vehicle.SeatCapacity, vehicle.ModelYear, vehicle.Type, vehicle.IsPremium, request.user.owner.OwnerID)
            execute_sql(sql, params)
            return redirect('garage_and_vehicle_list')

    else:
        garage_form = GarageForm()
        vehicle_form = VehicleForm()

    return render(request, 'add_gar_car.html', {'garage_form': garage_form, 'vehicle_form': vehicle_form})

def edit_garage(request, garage_id):
    sql = "SELECT * FROM Garage WHERE GarageID = %s"
    garage = execute_sql(sql, [garage_id])
    if not garage:
        return redirect('owner_dashboard')

    if request.method == 'POST':
        form = GarageForm(request.POST)
        if form.is_valid():
            sql = "UPDATE Garage SET Slots = %s, CCTV = %s, Watchmen = %s, Area = %s, Address = %s WHERE GarageID = %s"
            params = (form.cleaned_data['Slots'], form.cleaned_data['CCTV'], form.cleaned_data['Watchmen'], form.cleaned_data['Area'], form.cleaned_data['Address'], garage_id)
            execute_sql(sql, params)
            return redirect('owner_dashboard')
    else:
        form = GarageForm(initial={'Slots': garage[0][1], 'CCTV': garage[0][2], 'Watchmen': garage[0][3], 'Area': garage[0][4], 'Address': garage[0][5]})

    return render(request, 'edit_garage.html', {'form': form})

def edit_vehicle(request, vehicle_id):
    sql = "SELECT * FROM Vehicle WHERE LicenseNumber = %s"
    vehicle = execute_sql(sql, [vehicle_id])
    if not vehicle:
        return redirect('owner_dashboard')

    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            sql = "UPDATE Vehicle SET ModelName = %s, Color = %s, SeatCapacity = %s, ModelYear = %s, Type = %s, IsPremium = %s WHERE LicenseNumber = %s"
            params = (form.cleaned_data['ModelName'], form.cleaned_data['Color'], form.cleaned_data['SeatCapacity'], form.cleaned_data['ModelYear'], form.cleaned_data['Type'], form.cleaned_data['IsPremium'], vehicle_id)
            execute_sql(sql, params)
            return redirect('owner_dashboard')
    else:
        form = VehicleForm(initial={'ModelName': vehicle[0][1], 'Color': vehicle[0][2], 'SeatCapacity': vehicle[0][3], 'ModelYear': vehicle[0][4], 'Type': vehicle[0][5], 'IsPremium': vehicle[0][6]})

    return render(request, 'edit_vehicle.html', {'form': form})
