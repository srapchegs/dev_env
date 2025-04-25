from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.



def index(request):
    context = {
        'title': "Главная"
    }
    return render(request, 'main/index.html', context)

def catalog(request):
    context = {
        'title': "Блоки"
    }
    return render(request, 'main/catalog.html', context)

def bucket(request):
    context = {
        'title': "Корзина"
    }
    return render(request, 'main/bucket.html', context)

def detail(request):
    context = {
        'title': "Детальная страница товара"
    }
    return render(request, 'main/detail.html', context)

def purchase(request):
    context = {
        'title': "Личный кабинет"
    }
    return render(request, 'main/purchase.html', context)

def contacts(request):
    context = {
        'title': "Контакты"
    }
    return render(request, 'main/contacts.html', context)

def favorite(request):
    context = {
        'title': "Избранные"
    }
    return render(request, 'main/favorite.html', context)

def reviews(request):
    context = {
        'title': "Отзывы"
    }
    return render(request, 'main/reviews.html', context)

def cars(request):
    context = {
        'title': "Спец. техника"
    }
    return render(request, 'main/cars.html', context)

def about(request):
    return HttpResponse('Home page')
