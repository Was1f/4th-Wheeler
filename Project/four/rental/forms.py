from django import forms
from .models import Garage, Vehicle

class GarageForm(forms.ModelForm):
    class Meta:
        model = Garage
        fields = ['slots', 'cctv', 'watchmen', 'area', 'address']

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['modelname', 'color', 'seatcapacity', 'modelyear', 'type', 'ispremium']
