
# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .models import Garage, Vehicle, Owner, User,Trip,Parking
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout


def rent_car(request):
    # Fetch vehicles with only the existing columns
    vehicles = Vehicle.objects.raw('SELECT licensenumber, modelname, color, seatcapacity, modelyear, type, ispremium FROM Vehicle')

    # Precompute estimated fees based on the seat capacity
    cars_with_fees = []
    for vehicle in vehicles:
        estimated_fee = vehicle.seatcapacity * 50  # Example formula: 500 BDT per seat
        cars_with_fees.append({
            'vehicle': vehicle,
            'estimated_fee': estimated_fee
        })

    return render(request, 'rentcar.html', {'cars_with_fees': cars_with_fees})



#def rent_car(request):
 #   rent=Vehicle.objects.raw('SELECT * FROM Vehicle ')
  #  return render(request, 'rentcar.html', {'rent': rent})



def rent_garage(request):
    # Use the correct SQL to include the primary key
    garages = Garage.objects.raw('SELECT garageid, address, area, cctv, watchmen, slots FROM Garage')

    # Prepare the data to be passed to the template
    garages_with_fees = []
    for garage in garages:
        estimated_fee = garage.slots * 400  # Example calculation
        actual_fee = estimated_fee + 100;  # Assuming actual fee includes some additional cost
        garages_with_fees.append({
            'garage': garage,
            'estimated_fee': estimated_fee,
            'actual_fee': actual_fee
        })

    return render(request, 'rentgarage.html', {'garages_with_fees': garages_with_fees})




from django.db import connection  # Add this import


def history(request):
    user_id = request.user.id  # Assuming the user is logged in

    # Fetch past trips
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT t.TripID, t.Start, t.End, v.ModelName, 
                   CASE WHEN v.IsPremium THEN 4000 ELSE 3000 END AS Cost
            FROM Trip t
            JOIN Vehicle v ON t.LicensePlate = v.LicenseNumber
            WHERE t.CustomerID = %s
        ''', [user_id])
        trips = cursor.fetchall()

    # Fetch past parking records without cost
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT p.ParkingID, p.Start, p.End, g.Address 
            FROM Parking p
            JOIN Garage g ON p.GarageID = g.GarageID
            WHERE p.CustomerID = %s
        ''', [user_id])
        parking_records = cursor.fetchall()

    return render(request, 'history.html', {'trips': trips, 'parking_records': parking_records})


# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('profile')
#         else:
#             # Handle invalid login here
#             return render(request, 'login.html', {'error': 'Invalid credentials'})

#     return render(request, 'login.html')


#@login_required
def user_profile(request):
    user = request.user
    return render(request, 'userprofile.html', {'user': user})

def logout_view(request):
    auth_logout(request)  # Logs out the user
    return redirect('login')  # Redirects to the login page after logging out