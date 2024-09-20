from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from .models import Garage, Vehicle, Owner
from .forms import GarageForm, VehicleForm

from django.contrib.auth.decorators import login_required
@login_required
def vehicle_list(request):
    # Check if the logged-in user is an owner
    if hasattr(request.user, 'owner'):
        vehicles = Vehicle.objects.filter(owner=request.user.owner)  # Filter by the owner's vehicles
        return render(request, 'vehicle_list.html', {'vehicles': vehicles})
    else:
        # Redirect or show an error message if the user is not an owner
        return render(request, 'error.html', {'message': 'You are not an owner.'})


# List all garages for the owner
def garage_list(request):
    owner = request.user.owner  # Assuming the user is logged in and has an owner profile
    garages = Garage.objects.filter(owner=owner)
    return render(request, 'garage_list.html', {'garages': garages})

# List all vehicles for the owner
def vehicle_list(request):
    owner = request.user.owner
    vehicles = Vehicle.objects.filter(owner=owner)
    return render(request, 'vehicle_list.html', {'vehicles': vehicles})

# Add a new garage
def add_garage(request):
    if request.method == 'POST':
        form = GarageForm(request.POST)
        if form.is_valid():
            garage = form.save(commit=False)
            garage.owner = request.user.owner
            garage.save()
            return redirect('garage_list')
    else:
        form = GarageForm()
    return render(request, 'add_garage.html', {'form': form})

# Edit an existing garage
def edit_garage(request, garage_id):
    garage = get_object_or_404(Garage, pk=garage_id)
    if request.method == 'POST':
        form = GarageForm(request.POST, instance=garage)
        if form.is_valid():
            form.save()
            return redirect('garage_list')
    else:
        form = GarageForm(instance=garage)
    return render(request, 'edit_garage.html', {'form': form})

# Add a new vehicle
def add_vehicle(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.owner = request.user.owner
            vehicle.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm()
    return render(request, 'add_vehicle.html', {'form': form})

# Edit an existing vehicle
def edit_vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            return redirect('vehicle_list')
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'edit_vehicle.html', {'form': form})

