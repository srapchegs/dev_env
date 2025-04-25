from django.shortcuts import render

# Create your views here.

def detail(request):
    context = {
        'title': "Детальная страница товара"
    }
    return render(request, 'main/detail.html', context)

def catalog(request):
    context = {
        'title': "Блоки"
    }
    return render(request, 'main/catalog.html', context)
