from django.db import models

class User(models.Model):
    userid =models.AutoField(primary_key=True)
    password =models.CharField(max_length=100)
    firstname=models.CharField(max_length=50)
    lastname=models.CharField(max_length=50)
    phoneno=models.CharField(max_length=20)
    email =models.CharField(max_length=100,blank=True,null=True)
    nid =models.IntegerField()
    isowner=models.BooleanField(default=False)
    dob=models.DateField()

    class Meta:
        managed= False  
        db_table='User'  

class Owner(models.Model):
    ownerid=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    noofcars= models.IntegerField(null=True,blank=True)
    noofgarages=models.IntegerField(null=True,blank=True)
    verification= models.BooleanField(null=True)

    class Meta:
        managed= False
        db_table= 'Owner'

class Vehicle(models.Model):
    licensenumber=models.IntegerField(primary_key=True)
    modelname= models.CharField(max_length=100)
    color=models.CharField(max_length=50)
    seatcapacity=models.IntegerField()
    modelyear =models.IntegerField()
    type =models.CharField(max_length=50)
    ispremium =models.BooleanField(default=False)
    owner_id =models.ForeignKey(Owner,on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'Vehicle'

class Garage(models.Model):
    garageid=models.AutoField(primary_key=True)
    slots=models.IntegerField()
    cctv=models.BooleanField(default=False)
    watchmen= models.BooleanField(default=False)
    area=models.CharField(max_length=100)
    address=models.CharField(max_length=255)
    owner=models.ForeignKey(Owner,on_delete=models.CASCADE)

    class Meta:
        managed=False
        db_table='Garage'


class Parking(models.Model):
    parking_id = models.AutoField(primary_key=True)
    max_parking_time = models.IntegerField()
    customer = models.ForeignKey('User', on_delete=models.CASCADE)  # Assuming 'User' is the User model
    parking_type = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField()
    garage = models.ForeignKey('Garage', on_delete=models.CASCADE)
    reserve = models.ForeignKey('Reserve', on_delete=models.CASCADE)  # Assuming 'Reserve' is another model
    user_end = models.DateTimeField(null=True, blank=True)
    owner_end = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Parking'


class Trip(models.Model):
    trip_id = models.AutoField(primary_key=True)
    pick_up_area = models.CharField(max_length=255)
    drop_off = models.CharField(max_length=255)
    customer = models.ForeignKey('User', on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    license_plate = models.ForeignKey('Vehicle', on_delete=models.CASCADE, db_column='LicensePlate')  # Vehicle model reference
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)  # Assuming 'Booking' is another model
    user_end = models.DateTimeField(null=True, blank=True)
    owner_end = models.DateTimeField(null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'Trip'




class Booking(models.Model):
    booking_id = models.AutoField(primary_key=True)
    confirmation = models.BooleanField(default=False)
    user = models.ForeignKey('User', on_delete=models.CASCADE)  # Assuming 'User' is the User model
    vehicle = models.ForeignKey('Vehicle', on_delete=models.CASCADE, db_column='LicenseNo')  # Assuming 'Vehicle' is the Vehicle model

    class Meta:
        managed = False
        db_table = 'Booking'


class Reserve(models.Model):
    reserve_id = models.AutoField(primary_key=True)
    garage = models.ForeignKey('Garage', on_delete=models.CASCADE)
    reservation_time = models.DateTimeField()
    is_parking_available = models.BooleanField(default=True)
    cancel = models.BooleanField(default=False)
    accept = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'Reserve'
