from django.shortcuts import render
from django import forms
from django.db import connection
from datetime import datetime






DESTINATIONS={
 'Chattogram':211,
 'Khulna':132,
 'Rangpur':254,
 'Comilla':84,
 'Rajshahi':198,
 'Sylhet':199,
 'Bogra':164,
 'Natore':164,
 'Bandarban':250,
 'Savar':22,
}

class DestinationForm(forms.Form):
 destination=forms.ChoiceField(choices=[(key,key) for key in DESTINATIONS.keys()],label="Select Destination")


 pickup_point=forms.CharField(max_length=100,label="Pick Up Point")

def calculate_fee(distance):
 return distance*12+2000


def get_latest_booking_id():
 with connection.cursor() as cursor:
  cursor.execute("SELECT BookingID FROM Booking ORDER BY BookingID DESC LIMIT 1")

  result=cursor.fetchone()
  if result:
   return result[0]
  return None

def insert_into_trip(pickup_point,dropoff,booking_id):
 with connection.cursor() as cursor:
  
  cursor.execute("""
                 

   INSERT INTO Trip (PickUpArea,DropOff,BookingID) 
   VALUES (%s,%s,%s)
  """,[pickup_point,dropoff,booking_id])

def destination_view(request):
 if request.method=='POST':
  form=DestinationForm(request.POST)
  if form.is_valid():
   destination=form.cleaned_data['destination']
   pickup_point=form.cleaned_data['pickup_point']
   distance=DESTINATIONS[destination]
   fee=calculate_fee(distance)


   booking_id=get_latest_booking_id()
   if booking_id is not None:
    insert_into_trip(pickup_point,destination,booking_id)
   return render(request,'confirmation.html',{
    'destination':destination,
    'pickup_point':pickup_point,
    'fee':fee
   }) 
 else:
  form=DestinationForm()
 return render(request,'destination_form.html',{'form':form})

class ReservationForm(forms.Form):
 PARKING_TYPE_CHOICES=[
  

  ('regular','Regular Parking'),
  ('premium','Premium Parking')
 ]
 parking_duration=forms.IntegerField(min_value=1,label="Parking Duration (in hours)")
 reservation_time=forms.DateTimeField(label="Reservation Time",widget=forms.DateTimeInput(attrs={'type':'datetime-local'}))
 parking_type=forms.ChoiceField(choices=PARKING_TYPE_CHOICES,label="Parking Type")

def calculate_parking_fee(hours,parking_type):
 rate=70
 if parking_type=='premium':
  rate=120
 return hours*rate



def insert_into_reserve(garage_id,reservation_time):
 with connection.cursor() as cursor:
  cursor.execute("""
   INSERT INTO Reserve (GarageID,ReservationTime,IsParkingAvailable) 
   VALUES (%s,%s,%s)
  """,[garage_id,reservation_time,True])
  return cursor.lastrowid




def insert_into_parking(customer_id,parking_type,reserve_id):
 with connection.cursor() as cursor:
  cursor.execute("""
   INSERT INTO Parking (CustomerID,ParkingType,ReserveID) 
   VALUES (%s,%s,%s)
  """,[customer_id,parking_type,reserve_id])

def reservation_view(request):
 if request.method=='POST':
  
  form=ReservationForm(request.POST)
  if form.is_valid():
   parking_duration=form.cleaned_data['parking_duration']
   reservation_time=form.cleaned_data['reservation_time']
   parking_type=form.cleaned_data['parking_type']
   fee=calculate_parking_fee(parking_duration,parking_type)
   garage_id=1
   reserve_id=insert_into_reserve(garage_id,reservation_time)
   customer_id=request.user.id
   insert_into_parking(customer_id,parking_type,reserve_id)
   return render(request,'parkconfirmation.html',{
    'reserve_id':reserve_id,

    'parking_duration':parking_duration,
    'reservation_time':reservation_time,
    'parking_type':parking_type,
    'fee':fee
   })
 else:
  

  form=ReservationForm()
 return render(request,'reservation_form.html',{'form':form})
