from django.shortcuts import render
from cars.models import Cars
# Create your views here.

def cars(request):
    cars = Cars.objects.all()
    context = {
        "title": "Спец. техника",
        "cars": cars 
    }
    return render(request, 'cars/cars.html', context)
