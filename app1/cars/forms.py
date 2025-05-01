import re
from django import forms


class CreateCarsForm(forms.Form):
    bid_address = forms.CharField()
    date_rent = forms.CharField()
    car_id = forms.IntegerField()
