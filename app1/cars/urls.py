from django.urls import path
from cars import views  # Correct import from the cars app

app_name = "cars"

urlpatterns = [
    path('', views.cars, name="cars"),
    path('create_cars/', views.create_cars, name="create_cars"),
]
