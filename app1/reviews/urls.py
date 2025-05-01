from django.urls import path
from reviews import views

app_name = "reviews"

urlpatterns = [
    path('', views.reviews, name="reviews"),
    path('create_reviews/', views.create_reviews, name="create_reviews"),
]
