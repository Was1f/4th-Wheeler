from django.shortcuts import render, redirect
from django.db import connection
from .models import Garage, Vehicle
from .forms import GarageForm, VehicleForm

def run_sql(query,params=None):
 

 with connection.cursor() as cursor:
  cursor.execute(query,params)
  return cursor.fetchall()

def vehicle_list(request):
 
 query="SELECT * FROM Vehicle"
 all_vehicles=run_sql(query)
 return render(request,'vehicle_list.html',{'all_vehicles':all_vehicles})

def owner_dashboard(request):
 
 query_garages="SELECT * FROM Garage"
 all_garages=run_sql(query_garages)

 query_vehicles="SELECT * FROM Vehicle"
 all_vehicles=run_sql(query_vehicles)

 return render(request,'o_db.html',{'all_garages':all_garages,'all_vehicles':all_vehicles})



def owner_add(request):
 if request.method=='POST':
  
  garage_form=GarageForm(request.POST)

  vehicle_form=VehicleForm(request.POST)
  if 'add_garage' in request.POST and garage_form.is_valid():
   query="INSERT INTO Garage (Slots,CCTV,Watchmen,Area,Address,OwnerID) VALUES (%s,%s,%s,%s,%s,%s)"

   params=(garage_form.cleaned_data['Slots'],garage_form.cleaned_data['CCTV'],garage_form.cleaned_data['Watchmen'],garage_form.cleaned_data['Area'],garage_form.cleaned_data['Address'],request.user.owner.OwnerID)
   run_sql(query,params)



   return redirect('garage_and_vehicle_list')
  


  if 'add_vehicle' in request.POST and vehicle_form.is_valid():
   query="INSERT INTO Vehicle (LicenseNumber,ModelName,Color,SeatCapacity,ModelYear,Type,IsPremium,OwnerID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
   params=(vehicle_form.cleaned_data['LicenseNumber'],vehicle_form.cleaned_data['ModelName'],vehicle_form.cleaned_data['Color'],vehicle_form.cleaned_data['SeatCapacity'],vehicle_form.cleaned_data['ModelYear'],vehicle_form.cleaned_data['Type'],vehicle_form.cleaned_data['IsPremium'],request.user.owner.OwnerID)
   run_sql(query,params)


   return redirect('garage_and_vehicle_list')
 else:
  

  garage_form=GarageForm()
  vehicle_form=VehicleForm()
 return render(request,'add_gar_car.html',{'garage_form':garage_form,'vehicle_form':vehicle_form})

def edit_garage(request,garage_id):
 
 query="SELECT * FROM Garage WHERE GarageID=%s"
 garage_data=run_sql(query,[garage_id])

 if not garage_data:
  return redirect('owner_dashboard')
 if request.method=='POST':
  form=GarageForm(request.POST)

  if form.is_valid():
   query="UPDATE Garage SET Slots=%s,CCTV=%s,Watchmen=%s,Area=%s,Address=%s WHERE GarageID=%s"
   params=(form.cleaned_data['Slots'],form.cleaned_data['CCTV'],form.cleaned_data['Watchmen'],form.cleaned_data['Area'],form.cleaned_data['Address'],garage_id)
   run_sql(query,params)
   return redirect('owner_dashboard')
  

 else:
  form=GarageForm(initial={'Slots':garage_data[0][1],'CCTV':garage_data[0][2],'Watchmen':garage_data[0][3],'Area':garage_data[0][4],'Address':garage_data[0][5]})
 return render(request,'edit_garage.html',{'form':form})

def edit_vehicle(request,vehicle_id):
 query="SELECT * FROM Vehicle WHERE LicenseNumber=%s"
 vehicle_data=run_sql(query,[vehicle_id])


 if not vehicle_data:
  return redirect('owner_dashboard')
 if request.method=='POST':
  form=VehicleForm(request.POST)


  if form.is_valid():
   query="UPDATE Vehicle SET ModelName=%s,Color=%s,SeatCapacity=%s,ModelYear=%s,Type=%s,IsPremium=%s WHERE LicenseNumber=%s"
   
   
   params=(form.cleaned_data['ModelName'],form.cleaned_data['Color'],form.cleaned_data['SeatCapacity'],form.cleaned_data['ModelYear'],form.cleaned_data['Type'],form.cleaned_data['IsPremium'],vehicle_id)
   run_sql(query,params)
   return redirect('owner_dashboard')
  

 else:
  form=VehicleForm(initial={'ModelName':vehicle_data[0][1],'Color':vehicle_data[0][2],'SeatCapacity':vehicle_data[0][3],'ModelYear':vehicle_data[0][4],'Type':vehicle_data[0][5],'IsPremium':vehicle_data[0][6]})
 return render(request,'edit_vehicle.html',{'form':form})
