from django.shortcuts import render

# Create your views here.

def detail(request):
    context = {
        'title': "Детальная страница товара"
    }
    return render(request, 'product/detail.html', context)

def catalog(request):
    context = {
        'title': "Блоки"
    }
    return render(request, 'product/catalog.html', context)
