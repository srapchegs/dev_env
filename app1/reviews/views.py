from django.shortcuts import render
from reviews.models import Reviews
from django.shortcuts import redirect, render
from django.contrib import messages
from django.forms import ValidationError
from django.db import transaction
from reviews.forms import CreateReviewsForm

# Create your views here.

def reviews(request):
    if request.user.is_authenticated:
        form = None  # Если форма нужна только для неавторизованных
    else:        
        form = CreateReviewsForm()
    reviews = Reviews.objects.filter(is_published=True).order_by('-pk')
    context = {
        "title": "Отзывы",
        "reviews": reviews,
        'form': form, 
    }
    return render(request, 'reviews/reviews.html', context)

def create_reviews(request):
    form = CreateReviewsForm(data=request.POST)
    if form.is_valid():
        try:
            with transaction.atomic():
                user = request.user
                Reviews.objects.create(
                    user=user,
                    what_likes=form.cleaned_data['what_likes'],
                    what_modern=form.cleaned_data['what_modern'],
                    review=form.cleaned_data['review'],
                )
                messages.success(request, 'Заявка оформлена!')
                return redirect('reviews:reviews')
        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('reviews:reviews')
        