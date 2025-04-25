from django.urls import path
from cars import views  # Correct import from the cars app

app_name = "cars"

urlpatterns = [
    path('cars/', views.cars, name="cars"),
]
