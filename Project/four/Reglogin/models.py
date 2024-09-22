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