from django.shortcuts import redirect, render
from django.contrib import messages
from cars.models import Cars, CarsBid
from django.forms import ValidationError
from django.db import transaction
from cars.forms import CreateCarsForm

# Create your views here.

def cars(request):
    if request.user.is_authenticated:
        form = None  # Если форма нужна только для неавторизованных
    else:        
        form = CreateCarsForm()
    cars = Cars.objects.all()
    context = {
        "title": "Спец. техника",
        "cars": cars,
        'form': form,
    }
    return render(request, 'cars/cars.html', context)

def create_cars(request):
    form = CreateCarsForm(data=request.POST)
    if form.is_valid():
        try:
            with transaction.atomic():
                user = request.user
                car_id = form.cleaned_data['car_id']
                car = Cars.objects.get(id=car_id)
                CarsBid.objects.create(
                    user=user,
                    bid_address=form.cleaned_data['bid_address'],
                    date_rent=form.cleaned_data['date_rent'],
                    cars = car,
                )
                messages.success(request, 'Заявка оформлена!')
                return redirect('cars:cars')
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('cars:cars')
        