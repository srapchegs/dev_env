from django.shortcuts import redirect, render
from django.contrib import messages
from cars.models import Cars, CarsBid
from django.forms import ValidationError
from django.db import transaction
from cars.forms import CreateCarsForm
from django.core.mail import send_mail

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
                email_subject = "Новая заявка!"
                email_body = (
                    f"Клиент: {user.first_name} {user.last_name} ({user.email}, {user.phone})\n"
                    f"\nСроки: {form.cleaned_data['date_rent']}\n"
                    f"Адрес: {form.cleaned_data['bid_address']}\n"
                    f"Спец. техника: {car.name}\n"
                )
                print("EMAIL BODY:\n", email_body)
                messages.success(request, 'Заявка оформлена!')
                send_mail(
                    email_subject,
                    email_body,
                    "srapik614@gmail.com",
                    ["srapik614@gmail.com"],
                    fail_silently=False,
                )
                return redirect('cars:cars')
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('cars:cars')
        