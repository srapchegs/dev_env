"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from main import views

urlpatterns = [
    path('', views.index, name="index"),
    path('catalog/', views.catalog, name="catalog"),
    path('purchase/', views.purchase, name="purchase"),
    path('bucket/', views.bucket, name="bucket"),
    path('contacts/', views.contacts, name="contacts"),
    path('favorite/', views.favorite, name="favorite"),
    path('reviews/', views.reviews, name="reviews"),
    path('cars/', views.cars, name="cars"),
    path('detail/', views.detail, name="detail"),
]
