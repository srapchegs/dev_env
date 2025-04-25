from django.shortcuts import render
from django.http import HttpResponse
from product.models import Categories

# Create your views here.



def index(request):
    categories = Categories.objects.all()
    context = {
        'title': "Главная",
        'categories': categories,
    }
    return render(request, 'main/index.html', context)


def bucket(request):
    context = {
        'title': "Корзина"
    }
    return render(request, 'main/bucket.html', context)


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

def about(request):
    return HttpResponse('Home page')
