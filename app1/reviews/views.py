from django.shortcuts import render
from reviews.models import Reviews
# Create your views here.

def reviews(request):
    reviews = Reviews.objects.filter(is_published=True)
    context = {
        "title": "Отзывы",
        "reviews": reviews 
    }
    return render(request, 'reviews/reviews.html', context)
