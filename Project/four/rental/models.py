from django.db import models

class User(models.Model):
    userid = models.AutoField(primary_key=True)
    password = models.CharField(max_length=100)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    phoneno = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, blank=True, null=True)
    nid = models.IntegerField()
    isowner = models.BooleanField(default=False)
    dob = models.DateField()

    class Meta:
        managed = False  
        db_table = 'User'  

class Owner(models.Model):
    ownerid = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    noofcars = models.IntegerField(null=True, blank=True)
    noofgarages = models.IntegerField(null=True, blank=True)
    verification = models.BooleanField(null=True)

    class Meta:
        managed = False
        db_table = 'Owner'

class Vehicle(models.Model):
    licensenumber = models.AutoField(primary_key=True)
    modelname = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    seatcapacity = models.IntegerField()
    modelyear = models.IntegerField()
    type = models.CharField(max_length=50)
    ispremium = models.BooleanField(default=False)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'Vehicle'

class Garage(models.Model):
    garageid = models.AutoField(primary_key=True)
    slots = models.IntegerField()
    cctv = models.BooleanField(default=False)
    watchmen = models.BooleanField(default=False)
    area = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'Garage'

